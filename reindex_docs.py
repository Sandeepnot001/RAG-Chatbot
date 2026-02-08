import os
import shutil
from pathlib import Path
from backend.rag_engine import RAGService
from dotenv import load_dotenv

load_dotenv()

def reindex():
    print("--- Starting Re-indexing Process ---")
    
    vector_store_dir = Path("data/vector_stores/college_docs")
    if vector_store_dir.exists():
        print(f"Deleting existing vector store at {vector_store_dir}...")
        shutil.rmtree(vector_store_dir)
    
    print("Initializing fresh RAGService...")
    rag = RAGService()
    
    tmp_dir = Path("data/tmp")
    if not tmp_dir.exists():
        print("Error: data/tmp directory not found.")
        return
    
    files = list(tmp_dir.glob("*"))
    print(f"Found {len(files)} files to re-index.")
    
    for file_path in files:
        if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".docx", ".txt", ".csv"]:
            print(f"Processing {file_path.name}...")
            # Mocking metadata as it was originally provided during upload
            # In a real scenario, we might want to store this metadata somewhere else
            metadata = {
                "source": file_path.name,
                "department": "Unknown",
                "semester": "Unknown"
            }
            success = rag.process_document(str(file_path), metadata)
            if success:
                print(f"Successfully re-indexed {file_path.name}")
            else:
                print(f"Failed to re-index {file_path.name}")
    
    print("--- Re-indexing Complete ---")

if __name__ == "__main__":
    reindex()
