from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment (e.g., OPENAI_API_KEY)
load_dotenv()
#------------------------------------------------------------------------------------------------------------------------------
#LLM Creation->RAG Prompt


# LLM Initialization
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

RAG_PROMPT = """
You are a helpful and knowledgeable assistant.

Answer the user's question using the provided context when it is relevant.
When the context does not contain relevant information, answer using your general knowledge instead.

Speak naturally, clearly, and conversationally — like you're explaining it to a human.

Guidelines:
- When the context directly answers the question, prioritize it and summarize only what is relevant.
- Keep responses concise and focused rather than repeating the entire context.
- Base context-based answers strictly on the information provided.

- When the context partially addresses the question, explain what is known from the documents and complete the answer using general knowledge.
- When the context is empty or irrelevant, start the response with the following sentence exactly:
  "This question is not covered by the provided documents, so the following answer is based on general knowledge."
  Then continue with the answer.
- When multiple documents disagree, briefly mention the disagreement.
- Mention sources naturally only when it adds clarity or value.

Context:
{context}

Question:
{input}

Your answer:

"""

prompt = ChatPromptTemplate.from_template(RAG_PROMPT)
