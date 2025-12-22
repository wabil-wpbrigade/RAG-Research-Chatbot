from typing import Tuple, List
from langchain_core.documents import Document

from app.rag.rag import answer_question


class AdaptiveRAGController:
    """
    Always-on Adaptive RAG orchestrator.
    Phase 0: delegates to existing simple RAG.
    """

    def run(self, question: str) -> Tuple[str, List[Document]]:
        """
        Entry point for all RAG queries.
        """
        return answer_question(question)


adaptive_rag_controller = AdaptiveRAGController()
