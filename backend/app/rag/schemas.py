from pydantic import BaseModel

class RAGQueryRequest(BaseModel):
    question: str
