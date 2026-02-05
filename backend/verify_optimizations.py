
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag_engine import RAGService

def test_optimizations():
    print("Initializing RAG Service...")
    rag = RAGService()
    
    print("\n--- TEST 1: Static Replies (Zero Quota) ---")
    static_queries = ["hi", "ml", "AI"]
    for q in static_queries:
        start = time.time()
        ans, src = rag.answer_question(q)
        duration = time.time() - start
        print(f"Query: '{q}'")
        print(f"Answer: {ans.encode('ascii', 'ignore').decode('ascii')}")
        print(f"Time: {duration:.4f}s")
        if duration > 0.1:
            print("[FAIL] Static reply took too long")
        else:
            print("[PASS] Instant response")
            
    print("\n--- TEST 2: Caching (Zero Quota) ---")
    query = "What is the syllabus?"
    print(f"First Call: '{query}' (Simulating LLM call...)")
    # Mocking the cache for this test to avoid real LLM call if no docs
    rag.ANSWER_CACHE[query.lower()] = ("Cached Answer", [])
    
    start = time.time()
    ans, src = rag.answer_question(query)
    duration = time.time() - start
    print(f"Second Call: '{query}'")
    print(f"Answer: {ans}")
    print(f"Time: {duration:.4f}s")
    if duration > 0.1:
        print("[FAIL] Cache miss")
    else:
        print("[PASS] Instant cache hit")

    print("\n--- TEST 3: Config Check ---")
    llm = rag._get_llm()
    if hasattr(llm, 'max_output_tokens'): # Google
        print(f"Max Output Tokens (Google): {llm.max_output_tokens}")
        if llm.max_output_tokens == 120:
             print("[PASS] Token limit set to 120")
        else:
             print(f"[FAIL] Token limit is {llm.max_output_tokens}")
    elif hasattr(llm, 'max_tokens'): # OpenAI
         print(f"Max Tokens (OpenAI): {llm.max_tokens}")
         if llm.max_tokens == 120:
             print("[PASS] Token limit set to 120")
         else:
             print(f"[FAIL] Token limit is {llm.max_tokens}")

if __name__ == "__main__":
    test_optimizations()
