# app/config.py
import os

# === File & database paths ===
files_folder_path = r"C:\Users\dell\Desktop\UMT\7th semester\Research papers"
vector_database_path = r"C:\Users\dell\Documents\GitHub\RAG-CHAT-BOT\vector_database"

#=====API Key===============
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY is not set. Please set it in your .env file.")