import os
from typing import Any, List, Tuple

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from .llm_prompt import llm, prompt
from .vectorstore import retriever_database

#--------------------------------------------------------------------------------------------------------------------------
#Context Builder->Final RAG Chain-> Final Answer Question

def context_documents_retrieval_chain(
    llm: Any, prompt: ChatPromptTemplate) -> Any:
    """
    Inputs: LLM configuration and Prompt Template
    Returns: Document Context Chain
    """
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    return document_chain


def get_rag_chain(top_k: int = 8) -> Any:
    """
    Builds and returns the full RAG chain.

    This function:
    - Loads the vector database retriever
    - Creates the document-combination chain (LLM + prompt)
    - Wraps both into a retrieval chain used to answer user questions

    Returns:
        A LangChain retrieval chain object ready for querying.
    """
    retriever = retriever_database(top_k=top_k)
    document_chain = context_documents_retrieval_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=document_chain)
    return rag_chain


def answer_question(question: str, top_k: int = 8) -> Tuple[str, List[Document]]:
    """
    -Loads: Retrieval chain
    -Invokes: User question
    -Generates: User's reply and source of documents
    Returns: User answer and List of source documents
    """
    rag_chain = get_rag_chain(top_k=top_k)
    result = rag_chain.invoke({"input": question})

    answer = result.get("answer", "").strip()
    source_docs = result.get("context", [])

    # If the model hit our fallback message, hide sources
    if answer.startswith(
        "I couldn't find this information in the provided documents."):
        source_docs = []

    return answer, source_docs


def format_source(doc: Document) -> str:
    """
    Formats: Retrieved Document's meta data
    Returns: Cleaner visual representation of Document's info
    """
    md = doc.metadata or {}
    title = md.get("paper_title")
    if not title:
        source_path = md.get("source", md.get("filename", "unknown file"))
        title = os.path.splitext(os.path.basename(source_path))[0]

    return str(title)
