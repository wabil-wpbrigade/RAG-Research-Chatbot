from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os

from .config import files_folder_path, vector_database_path

#----------------------------------------------------------------------------------------------------------------------------------------
#Loading PDFs-> Chunking-> Embedding and Chunk Storage-> Ingestion





#load all the pdf files in the folder
def load_pdf_files(files_folder_path):
    All_pdf_files = []
    for files in os.listdir(files_folder_path):
        if files.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(files_folder_path, files))
            documents = loader.load()
            All_pdf_files.extend(documents)
    return All_pdf_files




#split the text into chunks
def split_text_into_chunks(All_pdf_files):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(All_pdf_files)
    return chunked_documents

#embed chunks and store in Vector Database
def embed_chunks_and_Vector_storage(chunked_documents):
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_database=Chroma.from_documents(
        documents=chunked_documents, 
        embedding=embedding_model, 
        persist_directory=vector_database_path
        )
    return vector_database




#ingestion process
def ingestion_process():
    All_pdf_files = load_pdf_files(files_folder_path)
    chunked_documents = split_text_into_chunks(All_pdf_files)
    vector_database = embed_chunks_and_Vector_storage(chunked_documents)
    return vector_database





if __name__ == "__main__":
    # Run this once (or when you add new PDFs)
    ingestion_process()