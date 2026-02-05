from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    department: Optional[str] = None
    semester: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

class DocumentMetadata(BaseModel):
    filename: str
    department: Optional[str] = None
    semester: Optional[str] = None
