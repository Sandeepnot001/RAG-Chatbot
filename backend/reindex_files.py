
import os
from pathlib import Path
from backend.rag_engine import RAGService

def reindex():
    print("Starting Re-indexing Process...")
    rag = RAGService()
    
    tmp_dir = Path("data/tmp")
    if not tmp_dir.exists():
        print("No temp directory found.")
        return

    files = [f for f in tmp_dir.iterdir() if f.is_file()]
    print(f"Found {len(files)} files to re-index.")

    for file_path in files:
        print(f"Processing {file_path.name}...")
        # Guess metadata or leave generic
        metadata = {
            "source": file_path.name,
            "reindexed": True
        }
        try:
            success = rag.process_document(str(file_path), metadata)
            if success:
                print(f"Successfully indexed {file_path.name}")
            else:
                print(f"Failed to index {file_path.name}")
        except Exception as e:
            print(f"Error indexing {file_path.name}: {e}")

    print("Re-indexing complete.")

if __name__ == "__main__":
    reindex()
