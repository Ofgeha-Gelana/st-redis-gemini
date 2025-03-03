from sentence_transformers import SentenceTransformer
import streamlit as st
import chromadb

# Initialize ChromaDB and embedding model
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="chat_history")

def view_documents(n_results=10):
    """Retrieve and display a limited number of documents stored in the collection."""
    # Retrieve all documents in the collection
    results = collection.get(include=["documents", "metadatas"])  # Removed 'ids' and used valid options

    # Print the documents, limiting the number of results
    st.write("Documents in the Collection:")
    for i, doc in enumerate(results["documents"][:n_results]):  # Slice to limit results
        st.write(f"Document {i+1}: {doc}")
        st.write(f"Metadata: {results['metadatas'][i]}")  # Optional: Show metadata if available

# Use this function in your Streamlit app to show data
view_documents()
