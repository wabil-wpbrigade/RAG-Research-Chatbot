from fastapi import APIRouter, Depends
from app.auth.dependencies import require_active_user
from app.rag.rag import answer_question
from app.db.models import User
from app.rag.schemas import RAGQueryRequest

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/query")
def query_rag(
    data: RAGQueryRequest,
    current_user: User = Depends(require_active_user),):
    answer, sources = answer_question(data.question)
    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in sources
        ],
    }
