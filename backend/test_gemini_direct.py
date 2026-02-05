
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key, transport="rest")

print("Testing Direct Gemini API (REST)...")
model = genai.GenerativeModel("gemini-2.0-flash")
try:
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
