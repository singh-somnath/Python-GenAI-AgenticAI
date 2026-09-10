from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
import os

def initiallizeVectorDB(documents,embedding_model):
        if not os.path.exists("vectordb/faiss"):
            os.makedirs("vectordb/faiss",exist_ok=True)
        dbFaiss = FAISS.from_documents(documents,embedding_model)
        dbFaiss.save_local(
               folder_path="vectordb/faiss"
        )

        if not os.path.exists("vectordb/chromadb"):
                os.makedirs("vectordb/chromadb",exist_ok=True)

        dbChroma = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory="vectordb/chromadb",
            collection_name="documents"
        )
    

def getVectorDB(embedding_model,type="FAISS"):
        if type == "FAISS":
              db = FAISS.load_local(
                     "vectordb/faiss",
                     embeddings=embedding_model,
                     allow_dangerous_deserialization=True)
        else:
              db = Chroma(
                     persist_directory="vectordb/chromadb",
                     embedding_function=embedding_model,
                     collection_name="documents")

        return db
       
