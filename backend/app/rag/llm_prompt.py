from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.rag.prompt_loader import load_rag_prompt

load_dotenv()

# LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.3, timeout=60, max_retries=2)

raw_prompt = load_rag_prompt("app/rag/rag_prompt.yaml")

prompt = ChatPromptTemplate.from_template(raw_prompt)
