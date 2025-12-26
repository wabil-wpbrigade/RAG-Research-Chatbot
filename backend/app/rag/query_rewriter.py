from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class QueryRewriter:
    """
    Rewrites vague or ambiguous queries into
    clearer, retrieval-optimized queries.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a query rewriting assistant for a Retrieval-Augmented Generation (RAG) system.

Rewrite the user's query to be:
- Clear
- Specific
- Optimized for document retrieval

Rules:
- Preserve original intent
- Do NOT add new information
- Do NOT answer the question
- Output ONLY the rewritten query text

User query:
{query}
"""
        )

    def rewrite(self, query: str) -> str:
        try:
            response = self.llm.invoke(
                self.prompt.format(query=query)
            )
            rewritten = response.content.strip()
            return rewritten if rewritten else query
        except Exception:
            return query
