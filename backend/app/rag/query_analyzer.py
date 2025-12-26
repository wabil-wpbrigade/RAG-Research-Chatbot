from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class QueryAnalysis(TypedDict):
    intent: str
    complexity: str
    needs_rewrite: bool


class QueryAnalyzer:
    """
    Lightweight query understanding component.
    Used by AdaptiveRAGController before retrieval.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a query analysis engine for a Retrieval-Augmented Generation (RAG) system.

Classify the user's query and return STRICT JSON only.

Allowed values:
- intent: factual | conceptual | procedural | exploratory
- complexity: low | medium | high
- needs_rewrite: true | false

Guidelines:
- factual: asks for a specific fact or definition
- conceptual: asks for explanations or understanding
- procedural: asks for steps or how-to
- exploratory: broad, vague, or research-style queries

Rewrite is needed if:
- the query is vague
- the query is ambiguous
- the query is poorly structured

User query:
{query}
"""
        )

    def analyze(self, query: str) -> QueryAnalysis:
        response = self.llm.invoke(
            self.prompt.format(query=query)
        )

        # LangChain returns an AIMessage
        content = response.content.strip()

        return self._safe_parse(content)

    def _safe_parse(self, content: str) -> QueryAnalysis:
        """
        Defensive parsing to avoid runtime crashes.
        """
        try:
            import json
            data = json.loads(content)

            return {
                "intent": data.get("intent", "conceptual"),
                "complexity": data.get("complexity", "medium"),
                "needs_rewrite": bool(data.get("needs_rewrite", False)),
            }
        except Exception:
            # Fail-safe defaults
            return {
                "intent": "conceptual",
                "complexity": "medium",
                "needs_rewrite": False,
            }
