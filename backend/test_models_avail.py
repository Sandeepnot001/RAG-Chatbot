
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key, transport="rest")

models_to_test = [
    "models/gemini-1.5-flash",
    "gemini-1.5-flash",
    "models/gemini-flash-latest",
    "models/gemini-pro",
    "models/gemini-1.5-pro"
]

for m in models_to_test:
    print(f"Testing {m}...")
    model = genai.GenerativeModel(m)
    try:
        response = model.generate_content("Hello")
        print(f"SUCCESS with {m}: {response.text}")
        break # Found one!
    except Exception as e:
        print(f"FAILED {m}: {e}")
