from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List, Optional
import os
import shutil
import traceback
from pathlib import Path
from datetime import timedelta

# Import our backend logic
try:
    from backend.auth import (
        router as auth_router, 
        get_current_user, 
        get_current_admin_user, 
        get_current_student_user,
        User,
        load_users,
        verify_password,
        create_access_token,
        ACCESS_TOKEN_EXPIRE_MINUTES,
        UserCreate
    )
    from backend.rag_engine import RAGService
except ImportError as e:
    print(f"CRITICAL: Import error during startup: {e}")
    traceback.print_exc()
    # Mocking basic dependencies if import fails to at least allow server to start for debugging
    raise e

app = FastAPI(title="CollegeBot API")

# Global Exception Handler to ensure JSON responses on all errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"ERROR: Unhandled exception during {request.method} {request.url}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"ERROR: Validation error during {request.method} {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation Error", "errors": exc.errors()}
    )

# Configure CORS for local development and Ngrok/Localtunnel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    print(f"RESPONSE: {response.status_code}")
    return response

# Initialize RAG Service lazily or at startup
rag_service = None
try:
    rag_service = RAGService()
except Exception as e:
    print(f"ERROR: Failed to initialize RAGService: {e}")
    traceback.print_exc()

# Root health check
@app.get("/")
async def root():
    return {"message": "FastAPI running on Vercel", "status": "healthy", "service": "online"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "rag_initialized": rag_service is not None}

# Explicitly define endpoints to match Frontend expectations exactly
@app.post("/api/login")
async def login_api(request: Request):
    # Try to get data from JSON or Form
    username = None
    password = None
    
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            data = await request.json()
            username = data.get("username")
            password = data.get("password")
        except:
            pass
    
    if not username:
        try:
            form_data = await request.form()
            username = form_data.get("username")
            password = form_data.get("password")
        except:
            pass

    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing username or password")

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
async def register_api(user_in: UserCreate):
    # This uses the imported register_user logic but as a clean FastAPI dependency
    from backend.auth import save_users
    users = load_users()
    if user_in.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    from backend.auth import pwd_context
    hashed_password = pwd_context.hash(user_in.password)
    new_user = {
        "username": user_in.username,
        "role": user_in.role,
        "hashed_password": hashed_password
    }
    
    users[user_in.username] = new_user
    save_users(users)
    return {"message": "User registered successfully"}

@app.post("/api/chat")
async def chat_api(
    data: dict, 
    current_user: User = Depends(get_current_student_user)
):
    if rag_service is None:
        raise HTTPException(status_code=503, detail="RAG Service is not initialized")
        
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
    if rag_service is None:
        raise HTTPException(status_code=503, detail="RAG Service is not initialized")

    temp_dir = Path("data/tmp")
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
    if rag_service is None:
        return {"documents": []}
    documents = rag_service.get_documents()
    return {"documents": documents}

@app.delete("/api/documents/{filename}")
async def delete_document_api(
    filename: str, 
    current_user: User = Depends(get_current_admin_user)
):
    if rag_service is None:
        raise HTTPException(status_code=503, detail="RAG Service is not initialized")
        
    success = rag_service.delete_document(filename)
    if success:
        return {"message": f"Document {filename} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete document")

@app.get("/api/stats")
async def get_stats_api(current_user: User = Depends(get_current_admin_user)):
    if rag_service is None:
        return {"total_documents": 0, "active_students": 0, "queries_today": 0}
    return rag_service.get_stats()

if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment variable (Render provides this)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
