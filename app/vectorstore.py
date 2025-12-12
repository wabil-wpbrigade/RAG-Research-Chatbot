# ruff: noqa: I001
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

from .injestion import vector_database_path


#--------------------------------------------------------------------------------------------------------------------------
#Get Database->make retriever->

def get_vector_database() -> Chroma:
    """
    Loads: the vector database created
    Returns: Vector Database
    """
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_database = Chroma(
        persist_directory=vector_database_path,
        embedding_function=embedding_model,
    )
    return vector_database


def retriever_database(top_k: int = 4) -> VectorStoreRetriever:
    """
    Calls Function:
        Loads: Existing Vector Database
        Returns: Vector Store Retriever
    """
    vector_database = get_vector_database()
    retriever = vector_database.as_retriever(search_kwargs={"k": top_k})
    return retriever
