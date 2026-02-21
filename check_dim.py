import os
import sys
from backend.rag_engine import RAGService
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def check_dim():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"Using model: models/gemini-embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key, transport="rest")
    vec = embeddings.embed_query("test")
    print(f"Dimension: {len(vec)}")

if __name__ == "__main__":
    check_dim()
