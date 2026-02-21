import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"), transport="rest")

print("Listing models...")
try:
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f"Embedding model: {m.name}")
        else:
            print(f"Generation model: {m.name}")
except Exception as e:
    print(f"Error: {e}")
