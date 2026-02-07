import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.models import QueryRequest, QueryResponse
from backend.rag_engine import RAGService

# Rate Limiter Imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

app = FastAPI(title="College Document Chatbot API")

# Rate Limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Service
rag_service = RAGService()

# Auth Router
from backend.auth import router as auth_router, get_current_admin_user, get_current_student_user, User
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    # Ensure directories exist
    os.makedirs("data/tmp", exist_ok=True)
    os.makedirs("data/vector_stores", exist_ok=True)

@app.get("/")
def root():
    return {"status": "Backend running", "service": "College Document Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(...),
    department: str = Form(...),
    semester: str = Form(...),
    current_user: User = Depends(get_current_admin_user)
):
    try:
        temp_path = f"data/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Metadata dict
        metadata = {
            "source": file.filename,
            "department": department,
            "semester": semester
        }
        
        # Trigger processing with metadata
        success = rag_service.process_document(temp_path, metadata)
        
        if success:
            # Generate summary
            summary = rag_service.generate_summary(temp_path)
            return {
                "message": f"Successfully uploaded {file.filename} for {department} - {semester}",
                "summary": summary
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to process document")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=QueryResponse)
@limiter.limit("5/minute")
async def chat_endpoint(
    request: Request, # Required for limiter
    body: QueryRequest,
    current_user: User = Depends(get_current_student_user)
):
    print(f"DEBUG: chat_endpoint received request: {body}")
    try:
        answer, sources = rag_service.answer_question(body.question)
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats(current_user: User = Depends(get_current_admin_user)):
    try:
        return rag_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
async def list_documents(current_user: User = Depends(get_current_admin_user)):
    try:
        return {"documents": rag_service.get_documents()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/documents/{filename}")
async def delete_document(filename: str, current_user: User = Depends(get_current_admin_user)):
    try:
        success = rag_service.delete_document(filename)
        if success:
            return {"message": f"Successfully deleted {filename}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete document")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
