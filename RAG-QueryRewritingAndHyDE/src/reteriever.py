from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.loader import getDocumentsChunks
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("OPENAI_API_KEY")
embeddingModel = OpenAIEmbeddings(model="text-embedding-3-small", api_key=apiKey)



def createReteriever(documentChunks):  
    try:
        if not os.path.exists("./store/vectorDbFaissOpenAI"):
            os.makedirs("./store/vectorDbFaissOpenAI")
        if not documentChunks:
             print("documentChunks required for FAISS")
             return ValueError("documentChunks required for FAISS")
        vDB =FAISS.from_documents(documentChunks,
                            embeddingModel,)
        
        vDB.save_local("./store/vectorDbFaissOpenAI")
        return vDB.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        print(e)

def loadReteriever():
    vDB = FAISS.load_local(
        "./store/vectorDbFaissOpenAI",
        embeddingModel,
        allow_dangerous_deserialization=True
    )
    return vDB.as_retriever(search_kwargs={"k": 5})


def getReteriever():
    try:
        if not os.path.exists("./store/vectorDbFaissOpenAI"):
            chunks = getDocumentsChunks()
            return createReteriever(chunks)
        else:
            return loadReteriever()
    except Exception as e:
            print(e)


