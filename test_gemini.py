# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")
# model_name = os.getenv("GEMINI_MODEL")

# # Check if API key exists
# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env")

# # Configure Gemini
# genai.configure(api_key=api_key)

# # Load model from .env
# model = genai.GenerativeModel(model_name)

# # Test prompt
# response = model.generate_content(
#     "Reply with exactly these two words: Gemini Connected"
# )

# print("Model:", model_name)
# print("Response:", response.text)