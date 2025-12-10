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
def get_rag_chain(top_k: int = 8):
    retriever=retriever_database(top_k=top_k)
    document_chain=context_documents_retrieval_chain(llm,prompt)
    rag_chain=create_retrieval_chain(
        retriever=retriever, 
        combine_docs_chain=document_chain
    )
    return rag_chain




#final_answer_question
FALLBACK_MESSAGE = "I couldn't find this information in the provided documents."

def answer_question(question: str, top_k: int = 8):
    rag_chain = get_rag_chain(top_k=top_k)
    result = rag_chain.invoke({"input": question})

    answer = result.get("answer", "").strip()
    source_docs = result.get("context", [])

    # If the model hit our fallback message, hide sources
    if answer.startswith(FALLBACK_MESSAGE):
        source_docs = []

    return answer, source_docs




import os

def format_source(doc):
    """Format a single Document's metadata into a human-friendly string."""
    md = doc.metadata or {}

    # Prefer the extracted paper title
    title = md.get("paper_title")
    if not title:
        # Fallback to filename if no title present
        source_path = md.get("source", md.get("filename", "unknown file"))
        title = os.path.splitext(os.path.basename(source_path))[0]

    return title
