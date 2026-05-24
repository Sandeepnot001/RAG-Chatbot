# RAG Chatbot 🤖

A simple Retrieval-Augmented Generation (RAG) chatbot that allows users to chat with their own documents using AI.

This project uses LangChain, Streamlit, vector database, and LLM APIs to answer questions based on uploaded files.

---

## 🚀 Features

- Upload documents (PDF, TXT, CSV, DOCX)
- Ask questions from your files
- AI answers based only on document content
- Semantic search using embeddings
- Simple Streamlit web interface
- Supports OpenAI / Gemini / Hugging Face models

---

## 🧠 How It Works

1. Upload a document  
2. Text is extracted and split into chunks  
3. Chunks are converted into embeddings  
4. Stored in a vector database (ChromaDB)  
5. User asks a question  
6. Relevant chunks are retrieved  
7. LLM generates final answer based on context  

---

## 🛠️ Tech Stack

- Python
- LangChain
- Streamlit
- ChromaDB
- OpenAI API / Google Gemini / Hugging Face

---

## 📂 Supported Files

- PDF
- TXT
- CSV
- DOCX

---

## ⚙️ Setup & Run

```bash
git clone <repo-link>
cd <project-folder>
pip install -r requirements.txt
streamlit run app.py

---

🔑 API Keys

Add API keys in the Streamlit sidebar:

OpenAI API Key OR
Google Gemini API Key OR
Hugging Face Token


----
📌 Note

This project is based on an open-source MIT licensed implementation and was used for learning and understanding RAG systems.
