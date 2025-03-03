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

def store_message(role, content):
    """Store chat messages in ChromaDB with unique IDs."""
    vector = embedding_model.encode(content).tolist()
    unique_id = str(uuid.uuid4())  # Generate a random unique ID

    collection.add(
        ids=[unique_id],  # Required unique ID
        documents=[content], 
        embeddings=[vector], 
        metadatas=[{"role": role}]
    )


def retrieve_context(user_input, top_k=3):
    """Retrieve the most relevant past messages for context."""
    vector = embedding_model.encode(user_input).tolist()
    results = collection.query(query_embeddings=[vector], n_results=top_k)
    
    past_messages = [doc for doc in results["documents"][0]]
    return "\n".join(past_messages)

def get_response(user_input):
    """Generate a response with context-aware retrieval from ChromaDB."""
    context = retrieve_context(user_input)
    full_prompt = f"Context:\n{context}\nUser: {user_input}\nAssistant:"
    
    response = get_gemini_response(full_prompt)

    # Store new messages
    store_message("user", user_input)
    store_message("assistant", response)

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
