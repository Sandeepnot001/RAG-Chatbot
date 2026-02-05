import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models_to_test = [
    "gemini-flash-latest",
    "gemini-2.5-flash-preview",
    "gemini-2.0-pro"
]

for model_name in models_to_test:
    print(f"\nTesting {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"[SUCCESS] {model_name} is working.")
    except Exception as e:
        print(f"[FAIL] {model_name}: {e}")

try:
    # Generate content
    response = model.generate_content("Hello Gemini")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")

print("Verification complete.")
