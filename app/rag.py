from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import os
from .vectorstore import retriever_database

#------------------------------------------------------------------------------------------------------------------------------
#LLM Creation->RAG Prompt




#Create LLM
llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.3)




#RAG Prompt Template
RAG_PROMPT = """
You are a helpful and knowledgeable assistant.  
Answer the user's question using ONLY the information provided in the context.  
Speak naturally, clearly, and conversationally — like you're explaining it to a human.

Important rules:
- If the context directly answers the question, give a clear and concise explanation.  
- Do NOT restate the entire context. Summarize only what is relevant.
- Do NOT invent or guess the answer. 
- If the answer is not in the context, say politely: "I couldn't find information about that in the documents you provided."

- If the context partially answers the question, explain what is known and what is missing.
- If multiple documents disagree, briefly mention the disagreement.
- Do not output citations in brackets. Instead, mention sources naturally only if helpful.

Context:
{context}

Question:
{input}

Your answer:

"""

prompt = ChatPromptTemplate.from_template(RAG_PROMPT)



#--------------------------------------------------------------------------------------------------------------------------
#Context Builder->Final RAG Chain-> Final Answer Question





#Context documents Retrieval 
def context_documents_retrieval_chain(llm,prompt):
    document_chain=create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
        )
    return document_chain



#final rag chain
def get_rag_chain(top_k: int = 6):
    retriever=retriever_database(top_k=top_k)
    document_chain=context_documents_retrieval_chain(llm,prompt)
    rag_chain=create_retrieval_chain(
        retriever=retriever, 
        combine_docs_chain=document_chain
    )
    return rag_chain




#final_answer_question
FALLBACK_MESSAGE = "I couldn't find this information in the provided documents."

def answer_question(question: str, top_k: int = 6):
    rag_chain = get_rag_chain(top_k=top_k)
    result = rag_chain.invoke({"input": question})

    answer = result.get("answer", "").strip()
    source_docs = result.get("context", [])

    # If the model hit our fallback message, hide sources
    if answer.startswith(FALLBACK_MESSAGE):
        source_docs = []

    return answer, source_docs




def format_source(doc):
    """Format a single Document's metadata into a human-friendly string."""
    md = doc.metadata or {}

    # File name only (no full path)
    source_path = md.get("source", "unknown file")
    filename = os.path.basename(source_path) if source_path else "unknown file"

    # Page info (prefer human page label if available)
    page_label = md.get("page_label")
    page = md.get("page")
    if page_label is not None:
        page_str = f"page {page_label}"
    elif page is not None:
        # page index is often 0-based, so add 1 if you want
        page_str = f"page {page + 1}"
    else:
        page_str = "page ?"

    # Author if available
    author = md.get("author")
    if author:
        author_str = f"by {author}"
    else:
        author_str = None

    parts = [filename, page_str]
    if author_str:
        parts.append(author_str)

    # Join parts like: "file.pdf – page 3 – by Hassan"
    return " – ".join(parts)