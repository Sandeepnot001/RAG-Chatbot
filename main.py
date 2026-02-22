from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import shutil
from pathlib import Path

# Import our backend logic
from backend.auth import (
    router as auth_router, 
    get_current_user, 
    get_current_admin_user, 
    get_current_student_user,
    User
)
from backend.rag_engine import RAGService

app = FastAPI(title="CollegeBot API")

# Configure CORS for local development and Ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Service
rag_service = RAGService()

# Root health check
@app.get("/")
async def root():
    return {"message": "FastAPI running on Vercel", "status": "healthy"}

# Include the authentication router
# Note: The frontend expects /api/login and /api/register
# but auth.router uses /token and /register.
# We will create explicit compatible endpoints.

@app.post("/api/login")
async def login_api(request: Request):
    # This matches the logic in api/login.py
    # and forwards to our existing auth logic or handles it directly
    from fastapi.security import OAuth2PasswordRequestForm
    from backend.auth import load_users, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
    from datetime import timedelta
    
    # Try to get data from JSON or Form
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
    except:
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    users = load_users()
    user_dict = users.get(username)
    
    if not user_dict or not verify_password(password, user_dict.get('hashed_password')):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username, "role": user_dict.get('role')}, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user_dict.get('role')
    }

@app.post("/api/register")
async def register_api(user_in: dict):
    from backend.auth import register_user, UserCreate
    return await register_user(UserCreate(**user_in))

@app.post("/api/chat")
async def chat_api(
    data: dict, 
    current_user: User = Depends(get_current_student_user)
):
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    answer, sources = rag_service.answer_question(question)
    return {"answer": answer, "sources": sources}

@app.post("/api/upload")
async def upload_api(
    file: UploadFile = File(...),
    department: str = Form(...),
    semester: str = Form(...),
    current_user: User = Depends(get_current_admin_user)
):
    temp_dir = Path("/tmp/data/tmp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / file.filename
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    metadata = {
        "source": file.filename,
        "department": department,
        "semester": semester
    }
    
    success = rag_service.process_document(str(temp_path), metadata)
    
    if success:
        summary = rag_service.generate_summary(str(temp_path))
        return {
            "message": f"Successfully uploaded {file.filename} for {department} - {semester}",
            "summary": summary
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to process document")

@app.get("/api/documents")
async def get_documents_api(current_user: User = Depends(get_current_admin_user)):
    documents = rag_service.get_documents()
    return {"documents": documents}

@app.delete("/api/documents/{filename}")
async def delete_document_api(
    filename: str, 
    current_user: User = Depends(get_current_admin_user)
):
    success = rag_service.delete_document(filename)
    if success:
        return {"message": f"Document {filename} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete document")

@app.get("/api/stats")
async def get_stats_api(current_user: User = Depends(get_current_admin_user)):
    return rag_service.get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
