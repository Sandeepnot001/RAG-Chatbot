
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag_engine import RAGService

def test_issue():
    print("Initializing RAG...")
    rag = RAGService()
    
    # Test case 1: "what is ml?" (Should ideally hit common response or RAG)
    # The issue is that it hits RAG but returns empty answer or cutoff answer?
    query = "what is ml?" 
    print(f"\nTesting query: '{query}'")
    answer, sources = rag.answer_question(query)
    
    print(f"Answer: '{answer}'")
    print(f"Sources: {sources}")
    
    if not answer:
        print("FAIL: Answer is empty")
    elif len(answer) < 10:
        print("WARNING: Answer is very short")
    else:
        print("SUCCESS: Got an answer")

if __name__ == "__main__":
    test_issue()
