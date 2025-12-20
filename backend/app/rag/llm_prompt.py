from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from jinja2 import Template

from app.rag.prompt_loader import load_rag_prompt

load_dotenv()

# LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

raw_prompt = load_rag_prompt("app/rag/rag_prompt.yaml")

prompt = ChatPromptTemplate.from_template(raw_prompt)
