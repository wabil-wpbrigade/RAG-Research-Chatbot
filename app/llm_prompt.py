from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment (e.g., OPENAI_API_KEY)
load_dotenv()
#------------------------------------------------------------------------------------------------------------------------------
#LLM Creation->RAG Prompt


# LLM Initialization
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

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
