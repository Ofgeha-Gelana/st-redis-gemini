# import streamlit as st
# import redis
# import google.generativeai as genai
# import json
# import os



# # Configure your Gemini API Key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Connect to Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# def get_gemini_response(prompt):
#     """Fetch response from Gemini API."""
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt)
#     return response.text if response else "Error fetching response."

# def get_response(prompt):
#     """Check Redis for cached response, else fetch from Gemini."""
#     cached_response = redis_client.get(prompt)
    
#     if cached_response:
#         return cached_response  # Return cached response
    
#     response = get_gemini_response(prompt)
#     redis_client.set(prompt, response, ex=86400)  # Cache response for 24 hours
#     return response

# # Streamlit UI
# st.title("AI Chat with Redis Cache")
# prompt = st.text_area("Enter your prompt:")

# if st.button("Get Response"):
#     if prompt:
#         response = get_response(prompt)
#         st.write("### Response:")
#         st.write(response)
#     else:
#         st.warning("Please enter a prompt.")




import streamlit as st
import redis
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
api_key = os.getenv("GEMINI_API_KEY")

# Debugging: Check if the API key is being loaded
if not api_key:
    st.error("Error: GEMINI_API_KEY not found. Check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def get_gemini_response(prompt):
    """Fetch response from Gemini API."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error fetching response."

def get_response(prompt):
    """Check Redis for cached response, else fetch from Gemini."""
    cached_response = redis_client.get(prompt)
    
    if cached_response:
        return cached_response  # Return cached response
    
    response = get_gemini_response(prompt)
    redis_client.set(prompt, response, ex=86400)  # Cache response for 24 hours
    return response

# Streamlit UI
st.title("AI Chat with Redis Cache")
prompt = st.text_area("Enter your prompt:")

if st.button("Get Response"):
    if prompt:
        response = get_response(prompt)
        st.write("### Response:")
        st.write(response)
    else:
        st.warning("Please enter a prompt.")
