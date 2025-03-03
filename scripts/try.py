import google.generativeai as genai

# Configure the API with your key
genai.configure(api_key="AIzaSyBao65U1wAfv7wH_xQL0gJ5KdKdftAywlk")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
