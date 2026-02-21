import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

load_dotenv()

print("DEBUG: Importing RAGService")
try:
    from backend.rag_engine import RAGService
    print("DEBUG: RAGService imported")
    
    print("DEBUG: Initializing RAGService")
    service = RAGService()
    print("DEBUG: RAGService initialized successfully")
    
    print("DEBUG: Testing intent detection")
    intent = service.determine_intent("Hello")
    print(f"DEBUG: Intent: {intent}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
