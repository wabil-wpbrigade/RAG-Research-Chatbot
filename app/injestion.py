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
    all_docs = []
    for filename in os.listdir(files_folder_path):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(files_folder_path, filename)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()  # list[Document]

        if not pages:
            continue

        # Try to use first non-empty line of first page as "title"
        first_page_text = pages[0].page_content or ""
        lines = [line.strip() for line in first_page_text.split("\n") if line.strip()]
        if lines:
            paper_title = lines[0][:200]  # avoid super long titles
        else:
            paper_title = os.path.splitext(filename)[0]

        # Attach metadata to every page
        for p in pages:
            p.metadata["paper_title"] = paper_title
            p.metadata["filename"] = filename  # optional, fallback

        all_docs.extend(pages)

    return all_docs





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