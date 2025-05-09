import streamlit as st
import redis
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and Redis credentials
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Error: GEMINI_API_KEY not found. Check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_gemini_response(history):
    """Fetch response from Gemini API with context."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(history)
    return response.text if response else "Error fetching response."

def get_response(user_input):
    """Check Redis for cached conversation, else fetch from Gemini."""
    conversation_key = "chat_history"

    # Retrieve previous conversation from Redis
    cached_history = redis_client.get(conversation_key)
    history = json.loads(cached_history) if cached_history else []

    # Append user input to history
    history.append({"role": "user", "content": user_input})

    # Generate AI response with full context
    full_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    response = get_gemini_response(full_context)

    # Append AI response to history
    history.append({"role": "assistant", "content": response})

    # Cache updated conversation
    redis_client.set(conversation_key, json.dumps(history), ex=86400)  # 24-hour cache

    return response

# Streamlit UI
st.title("AI Chat with Context & Redis Cache")

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
    st.session_state.chat_history = []
    redis_client.delete("chat_history")
    st.success("Chat history cleared.")
