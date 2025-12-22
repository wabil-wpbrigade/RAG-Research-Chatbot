from fastapi import APIRouter, Depends
from app.auth.dependencies import require_active_user
from app.rag.controller import adaptive_rag_controller
from app.db.models import User
from app.rag.schemas import RAGQueryRequest

router = APIRouter(prefix="/rag", tags=["rag"])


def format_sources(docs):
    return [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in docs
    ]


@router.post("/query")
def query_rag(
    data: RAGQueryRequest,
    current_user: User = Depends(require_active_user),):
    answer, sources = adaptive_rag_controller.run(data.question)
    return {"answer": answer, "sources": format_sources(sources)}
