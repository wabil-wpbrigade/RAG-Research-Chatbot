from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from .config import vector_database_path


#--------------------------------------------------------------------------------------------------------------------------
#Get Database->make retriever->


#get vector database
def get_vector_database():
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_database = Chroma(
        persist_directory=vector_database_path, 
        embedding_function=embedding_model)
    return vector_database

#Make vector database into retriever
def retriever_database(top_k: int=4):
    vector_database=get_vector_database()
    retriever=vector_database.as_retriever(search_kwargs={"k": top_k})
    return retriever