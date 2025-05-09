import streamlit as st
import google.generativeai as genai
import chromadb
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Retrieve API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Error: GEMINI_API_KEY not found. Check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize ChromaDB and embedding model
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="chat_history")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, efficient embedding model

def get_gemini_response(history):
    """Fetch response from Gemini API with context."""
    # model = genai.GenerativeModel("gemini-pro")
    model = genai.GenerativeModel("gemini-1.5-pro") ## added after error raised

    response = model.generate_content(history)
    return response.text if response else "Error fetching response."

# def store_message(role, content):
#     """Store chat messages in ChromaDB."""
#     vector = embedding_model.encode(content).tolist()
#     collection.add(
#         documents=[content], 
#         embeddings=[vector], 
#         metadatas=[{"role": role}]
#     )


import uuid  # Import UUID to generate unique IDs

def store_message(role, content, msg_id=None, pair_id=None):
    """Store chat messages in ChromaDB with optional ID linking."""
    vector = embedding_model.encode(content).tolist()
    unique_id = msg_id or str(uuid.uuid4())  # Use given ID or generate new one

    metadata = {"role": role}
    if pair_id:
        metadata["pair_id"] = pair_id

    collection.add(
        ids=[unique_id],
        documents=[content],
        embeddings=[vector],
        metadatas=[metadata]
    )


def retrieve_context(user_input, top_k=3):
    """Retrieve the most relevant past messages for context."""
    vector = embedding_model.encode(user_input).tolist()
    results = collection.query(query_embeddings=[vector], n_results=top_k)
    
    past_messages = [doc for doc in results["documents"][0]]
    return "\n".join(past_messages)


def maybe_get_cached_response(user_input, similarity_threshold=0.9):
    """Try to find a previous similar user message and return its paired assistant reply."""
    vector = embedding_model.encode(user_input).tolist()
    results = collection.query(query_embeddings=[vector], n_results=1)

    if not results["documents"] or not results["metadatas"]:
        return None

    doc = results["documents"][0][0]
    meta = results["metadatas"][0][0]

    if meta["role"] != "user":
        return None

    user_msg_id = results["ids"][0][0]
    
    # Find the paired assistant response
    assistant_results = collection.get(where={"pair_id": user_msg_id})
    if assistant_results and assistant_results["documents"]:
        return assistant_results["documents"][0]
    
    return None

def get_response(user_input):
    # Check for a similar past user message and use cached reply
    cached = maybe_get_cached_response(user_input)
    if cached:
        return cached

    # Otherwise proceed with context + Gemini
    context = retrieve_context(user_input)
    full_prompt = f"Context:\n{context}\nUser: {user_input}\nAssistant:"
    response = get_gemini_response(full_prompt)

    # Store both messages with paired IDs
    user_id = str(uuid.uuid4())
    assistant_id = str(uuid.uuid4())

    store_message("user", user_input, msg_id=user_id, pair_id=assistant_id)
    store_message("assistant", response, msg_id=assistant_id, pair_id=user_id)

    return response


# Streamlit UI
st.title("AI Chat with ChromaDB Memory")

user_input = st.text_area("Enter your message:")

if st.button("Send"):
    if user_input:
        response = get_response(user_input)
        st.write("### Response:")
        st.write(response)
    else:
        st.warning("Please enter a message.")

# Reset button to clear context
if st.button("Reset Chat"):
    # collection.delete(where={})   # Clears stored messages
    collection.delete(where={"$exists": True})  # Deletes all documents in the collection
    st.success("Chat history cleared.")
