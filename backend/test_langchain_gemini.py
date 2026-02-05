
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("Testing LangChain Gemini Wrapper...")
# Try with current settings
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.3,
    client_options={"transport": "rest"}
)

try:
    response = llm.invoke("Hello")
    print(f"Success! Response: {response.content}")
except Exception as e:
    print(f"Error: {e}")
