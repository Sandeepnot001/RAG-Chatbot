import os
import sys
from backend.rag_engine import RAGService
from backend.models import QueryRequest

def test_query():
    print("Initializing RAGService...")
    rag = RAGService()
    question = "cyberecurity"
    print(f"Testing question: {question}")
    try:
        answer, sources = rag.answer_question(question)
        print(f"Answer: {answer}")
        print(f"Sources: {sources}")
    except Exception as e:
        print(f"FAILED with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_query()
