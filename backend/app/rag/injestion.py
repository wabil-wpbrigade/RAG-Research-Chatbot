import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# === File & database paths ===
files_folder_path = r"C:\Users\dell\Desktop\UMT\7th semester\Research papers"
vector_database_path = "/app/vector_database"

#----------------------------------------------------------------------------------------------------------------------------------------
#Loading PDFs-> Chunking-> Embedding and Chunk Storage-> Ingestion

def load_pdf_files(files_folder_path: str) -> list[Document]:
    """
    Loads: All files with .pdf extension
    Returns: List of Document Objects
    """
    all_pdf_files = []
    for file in os.listdir(files_folder_path):
        if file.lower().endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(files_folder_path, file))
            documents = loader.load()
            all_pdf_files.extend(documents)
    return all_pdf_files


def split_text_into_chunks(All_pdf_files: list[Document]) -> list[Document]:
    """
    Splits: Text from Documents into chunks
    Returns: Chunked Documents
    """
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(All_pdf_files)
    return chunked_documents

def embed_chunks_and_Vector_storage(chunked_documents: list[Document]) -> Chroma:
    """
    Embeds: Chunked Documents into Vector Database
    Returns: Vector Database
    """
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_database = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embedding_model,
        persist_directory=vector_database_path,
    )
    return vector_database

def ingestion_process()->Chroma:
    """
    Calls Functions:

        Loads: All files with .pdf extension
        Splits: Text from Documents into chunks
        Embeds: Chunked Documents into Vector Database
        Returns: Vector Database
    """
    All_pdf_files = load_pdf_files(files_folder_path)
    chunked_documents = split_text_into_chunks(All_pdf_files)
    vector_database = embed_chunks_and_Vector_storage(chunked_documents)
    return vector_database


if __name__ == "__main__":
    """
    Calls Function:
        Injestion Process
    """
    ingestion_process()
