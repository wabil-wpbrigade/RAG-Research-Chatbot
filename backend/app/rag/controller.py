from typing import Tuple, List
from langchain_core.documents import Document

from app.rag.rag import answer_question
from app.rag.query_analyzer import QueryAnalyzer
from app.rag.query_rewriter import QueryRewriter
from app.rag.retrieval_policy import determine_top_k



class AdaptiveRAGController:
    """
    Adaptive RAG Orchestrator
    """
    def __init__(self):
        self.query_analyzer = QueryAnalyzer()
        self.query_rewriter = QueryRewriter()
        self._last_analysis = None
        self._rewritten_query = None


    def run(self, question: str) -> Tuple[str, List[Document]]:
        """
        Entry point for all RAG queries.
        """
        cleaned_question = self._preprocess_question(question)

        answer, documents = self._retrieve_and_generate(cleaned_question)

        answer, documents = self._postprocess_answer(answer, documents)

        return answer, documents

    # -----------------------
    # Internal pipeline steps
    # -----------------------

    def _preprocess_question(self, question: str) -> str:
        """
        Phase 3:
        - Analyze query
        - Rewrite if flagged
        """
        analysis = self.query_analyzer.analyze(question)
        self._last_analysis = analysis

        if analysis.get("needs_rewrite", False):
            rewritten = self.query_rewriter.rewrite(question)
            self._rewritten_query = rewritten
            return rewritten

        return question



    def _retrieve_and_generate(self, question: str):
        """
        Phase 2:
        - Adaptive retrieval depth based on query analysis
        """
        analysis = self._last_analysis or {}

        intent = analysis.get("intent", "conceptual")
        complexity = analysis.get("complexity", "medium")

        top_k = determine_top_k(intent, complexity)

        return answer_question(question, top_k=top_k)


    def _postprocess_answer(self, answer: str, documents: List[Document]) -> Tuple[str, List[Document]]:
        """
        Phase 0:
        - No postprocessing
        - Reserved for validation / correction
        """
        return answer, documents


adaptive_rag_controller = AdaptiveRAGController()
