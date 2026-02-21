import sys
import time

def test_import(module_name):
    print(f"DEBUG: Testing import of {module_name}...", end="", flush=True)
    start = time.time()
    try:
        __import__(module_name)
        print(f" Success! ({time.time() - start:.2f}s)", flush=True)
    except Exception as e:
        print(f" Failed! Error: {e}", flush=True)

modules = [
    "os",
    "pathlib",
    "typing",
    "json",
    "dotenv",
    "fastapi",
    "uvicorn",
    "google.generativeai",
    "langchain_community.document_loaders",
    "langchain_text_splitters",
    "langchain_community.vectorstores",
    "langchain_google_genai",
    "langchain_openai",
    "langchain_community.embeddings",
    "langchain_classic.chains",
    "langchain_classic.memory",
    "langchain_core.prompts",
    "langchain_core.documents"
]

print("--- Diagnostic Import Test ---", flush=True)
for mod in modules:
    test_import(mod)
print("--- Diagnostic Complete ---", flush=True)
