
import os
from dotenv import load_dotenv
from backend.rag_engine import RAGService

load_dotenv()

print("Initializing RAG Service...")
rag = RAGService()
print("RAG Service Initialized.")

print("Testing General Chat...")
answer, sources = rag.answer_question("Hello! Who are you?")
print(f"Answer: {answer}")
print(f"Sources: {sources}")
