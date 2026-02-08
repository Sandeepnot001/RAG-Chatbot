import json
from pathlib import Path
from typing import List, Tuple

# Langchain imports
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
    CSVLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

import os
from dotenv import load_dotenv

load_dotenv()


import google.generativeai as genai
# Configure global genai to use REST to avoid GRPC hangs
genai.configure(transport="rest")

class RAGService:
    def __init__(self):
        self.tmp_dir = Path("data/tmp")
        self.vector_store_dir = Path("data/vector_stores/college_docs")
        
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store_dir.parent.mkdir(parents=True, exist_ok=True)
        
        self.stats_file = Path("data/stats.json")
        print("DEBUG: Starting RAGService initialization", flush=True)
        self._init_stats_file()
        print("DEBUG: Stats file initialized", flush=True)
        
        
        # Configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "Google") # Google, OpenAI, HuggingFace
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize components
        print("DEBUG: Getting embeddings", flush=True)
        self.embeddings = self._get_embeddings()
        print("DEBUG: Embeddings initialized", flush=True)
        print("DEBUG: Getting vector store", flush=True)
        self.vector_store = self._get_vector_store()
        print("DEBUG: Vector store initialized", flush=True)
        self.llm = self._get_llm() # Unified LLM instance for Chains
        print("DEBUG: LLM initialized", flush=True)
        self.genai_model = genai.GenerativeModel("gemini-flash-latest") # Direct model for robust operations
        print("DEBUG: GenAI model initialized", flush=True)
        
        # Shared Memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create Chains
        self.academic_chain = self._create_academic_chain()

    def _get_embeddings(self):
        # Using the verified correct model name for this account
        return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=self.google_api_key, transport="rest")

    def _get_vector_store(self):
        # Initialize Chroma
        if self.vector_store_dir.exists() and any(self.vector_store_dir.iterdir()):
             return Chroma(persist_directory=str(self.vector_store_dir), embedding_function=self.embeddings)
        else:
             return Chroma(persist_directory=str(self.vector_store_dir), embedding_function=self.embeddings)

    def _get_llm(self):
        print("DEBUG: Initializing LLM")
        # Reduced max_output_tokens to 150 for quota optimization
        if self.llm_provider == "Google":
            return ChatGoogleGenerativeAI(
                model="models/gemini-flash-latest",
                google_api_key=self.google_api_key,
                temperature=0.3,
                max_output_tokens=1024, 
            )
        elif self.llm_provider == "OpenAI":
            return ChatOpenAI(
                 model="gpt-3.5-turbo",
                 api_key=self.openai_api_key,
                 temperature=0.3,
                 max_tokens=512
            )
        else:
            return ChatGoogleGenerativeAI(
                model="models/gemini-flash-latest",
                google_api_key=self.google_api_key,
                temperature=0.3,
                transport="rest",
                max_output_tokens=1024,
            )

    # [RESTORED METHOD]
    def _create_academic_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        template = """You are CollegeBot, an intelligent academic assistant.
        
        MODE: ACADEMIC_DOCUMENT_QUERY
        
        INSTRUCTIONS:
        1. Context Usage: Priority is given to the provided Context.
        2. Not Found: If the answer is NOT in the Context, you MAY use your own general knowledge to answer, but you MUST preface it with: "I could not find this specific information in the uploaded documents, but here is a general answer:".
        3. Structure: Explain step-by-step. Use headings and bullet points.
        4. Citations: If you use the Context, you MUST cite the document name and page number.
           Format: [Source: filename (Page X)]
        
        Context: {context}
        Chat History: {chat_history}
        Question: {question}
        
        Answer:"""
        
        prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": prompt},
            verbose=True
        )

    # [RESTORED METHOD]
    def determine_intent(self, question: str) -> str:
        prompt = f"""
        Classify the intent of this user query into one of two categories:
        1. GENERAL_CHAT: Greetings, small talk, definitions of general concepts (e.g. "what is ML?", "explain AI"), general advice.
        2. ACADEMIC_DOCUMENT_QUERY: Questions specifically verifying details from uploaded files, syllabus, units, regulations, or asking about specific "files" or "documents".
        
        Query: "{question}"
        
        Return ONLY the category name.
        """
        try:
            print(f"DEBUG: Calling genai_model for intent detection...", flush=True)
            response = self.genai_model.generate_content(prompt)
            content = response.text.strip().upper()
            if "ACADEMIC" in content or "DOCUMENT" in content:
                return "ACADEMIC_DOCUMENT_QUERY"
            return "GENERAL_CHAT"
        except Exception as e:
            print(f"DEBUG ERROR intent: {e}")
            return "GENERAL_CHAT"

    # [RESTORED METHOD]
    def process_document(self, file_path: str, metadata: dict = None) -> bool:
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_ext == ".txt":
                loader = TextLoader(file_path)
            elif file_ext == ".csv":
                loader = CSVLoader(file_path, encoding="utf8")
            elif file_ext == ".docx":
                loader = Docx2txtLoader(file_path)
            else:
                return False
                
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            
            if metadata:
                for chunk in chunks:
                    chunk.metadata.update(metadata)
            
            self.vector_store.add_documents(chunks)
            self.vector_store.persist()
            self.academic_chain = self._create_academic_chain()
            return True
        except Exception as e:
            print(f"Error processing document: {e}")
            return False

    # [RESTORED METHOD]
    def generate_summary(self, file_path: str) -> str:
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_ext == ".txt":
                loader = TextLoader(file_path)
            elif file_ext == ".docx":
                loader = Docx2txtLoader(file_path)
            else:
                return "Unsupported file type."

            documents = loader.load()
            if not documents: return "Empty."

            full_text = "\n".join([doc.page_content for doc in documents[:5]]) 
            if len(full_text) > 10000: full_text = full_text[:10000] + "..."

            summary_prompt = f"Summary (max 3-4 bullets):\n\n{full_text}"
            response = self.genai_model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            return "Could not generate summary."

    # Optimization 1 & 2: Common Responses & Local Cache
    COMMON_RESPONSES = {
        "hi": "Hello 👋 How can I help you today?",
        "hello": "Hi 😊 Ask me anything.",
        "ml": "Machine Learning is a branch of Artificial Intelligence that enables systems to learn from data.",
        "what is ml": "Machine Learning is a branch of Artificial Intelligence that enables systems to learn from data.",
        "ai": "Artificial Intelligence is the ability of machines to perform tasks that require human intelligence.",
        "what is ai": "Artificial Intelligence is the ability of machines to perform tasks that require human intelligence."
    }
    ANSWER_CACHE = {}

    def answer_question(self, question: str) -> Tuple[str, List[str]]:
        print(f"DEBUG: answer_question called with: {question}", flush=True)
        
        import string
        # Robust query normalization: remove punctuation, lower, strip
        q_lower = question.lower().translate(str.maketrans('', '', string.punctuation)).strip()
        
        # Increment real stats
        self._increment_query_count()
        
        # 1. Check Common Responses (Zero Quota)
        if q_lower in self.COMMON_RESPONSES:
            print("DEBUG: Returning Common Response")
            return self.COMMON_RESPONSES[q_lower], []
            
        # 2. Check Local Cache (Zero Quota)
        if q_lower in self.ANSWER_CACHE:
            print("DEBUG: Returning Cached Response")
            return self.ANSWER_CACHE[q_lower]

        try:
            if not self.academic_chain:
                 pass

            # 3. Smart Fallback (No extra LLM call)
            # Search DB first. If good match -> Academic. Else -> General.
            # Using k=1 to check relevance score.
            # Note: Chroma L2 distance: Lower is better. 0 = identical. > 1 = unrelated.
            # Threshold: 0.7 (Tunable)
            
            docs_and_scores = self.vector_store.similarity_search_with_score(question, k=1)
            
            is_academic = False
            if docs_and_scores:
                doc, score = docs_and_scores[0]
                print(f"DEBUG: Best Doc Score (Distance): {score} - {doc.metadata.get('source')}")
                if score < 1.2: # Chroma default is L2. A safe bet for "relevant enough" is usually under 1.4 for embeddings. 1.2 is tight.
                     is_academic = True
            
            answer = ""
            sources = []

            if is_academic:
                print("DEBUG: Mode -> ACADEMIC (Based on vector score)")
                response = self.academic_chain.invoke({"question": question})
                answer = response["answer"]
                source_docs = response.get("source_documents", [])
                sources = [
                    f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 0)})" 
                    for doc in source_docs
                ]
                sources = list(set(sources))
            else:
                print("DEBUG: Mode -> GENERAL (Low vector score or no docs)")
                # Manual General Chat
                history = self.memory.load_memory_variables({})['chat_history']
                general_prompt = f"""You are CollegeBot. Be friendly and concise (max 2 sentences).
                Chat History: {history}
                Question: {question}
                Answer:"""
                
                # Reduced tokens for general chat
                response = self.genai_model.generate_content(
                    general_prompt, 
                    generation_config=genai.types.GenerationConfig(max_output_tokens=60)
                )
                answer = response.text
                self.memory.save_context({"question": question}, {"answer": answer})
                sources = []

            # Update Cache
            self.ANSWER_CACHE[q_lower] = (answer, sources)
            return answer, sources

        except Exception as e:
            print(f"DEBUG ERROR in answer_question: {e}")
            error_msg = str(e)
            if "429" in error_msg or "Quota exceeded" in error_msg or "ResourceExhausted" in error_msg:
                return "I'm currently receiving too many requests (Quota Exceeded). Please wait 30-60 seconds and try again.", []
            return "Sorry, I encountered an internal error. Please try again later.", []

    # [NEW METHOD]
    def delete_document(self, filename: str) -> bool:
        """
        Deletes a document from the vector store by its source filename.
        """
        try:
            print(f"DEBUG: Deleting document with source: {filename}")
            # ChromaDB delete by where clause
            self.vector_store.delete(where={"source": filename})
            self.vector_store.persist()
            
            # Also remove from cache if exists (optional, but good practice)
            # Clearing entire cache is safer/easier than finding specific keys
            self.ANSWER_CACHE.clear() 
            
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

    def get_documents(self) -> List[dict]:
        """
        Retrieves a list of unique documents from the vector store metadata.
        """
        try:
            # Helper: List all files in the vector store is semantic, but usually we just want what we uploaded.
            # Using collection.get() is the way.
            data = self.vector_store.get() 
            metadatas = data['metadatas']
            
            unique_docs = {}
            for m in metadatas:
                if m is None: continue
                source = m.get('source')
                if source and source not in unique_docs:
                    unique_docs[source] = {
                        "name": source,
                        "department": m.get('department', 'Unknown'),
                        "semester": m.get('semester', 'Unknown')
                    }
            
            return list(unique_docs.values())
        except Exception as e:
            print(f"Error getting documents: {e}")
            return []

    # [STATS METHODS]
    def _init_stats_file(self):
        if not self.stats_file.parent.exists():
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.stats_file.exists():
            with open(self.stats_file, 'w') as f:
                json.dump({"total_queries": 0, "unique_students": 12}, f) # Start with base mock for students

    def _get_persistent_stats(self):
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {"total_queries": 0, "unique_students": 12}

    def _increment_query_count(self):
        stats = self._get_persistent_stats()
        stats["total_queries"] += 1
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f)

    def get_stats(self) -> dict:
        """
        Returns system statistics.
        """
        docs = self.get_documents()
        p_stats = self._get_persistent_stats()
        return {
            "total_documents": len(docs),
            "active_students": p_stats.get("unique_students", 0),
            "queries_today": p_stats.get("total_queries", 0)
        }
