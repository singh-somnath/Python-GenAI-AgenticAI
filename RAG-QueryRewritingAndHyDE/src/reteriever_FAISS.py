from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("OPENAI_API_KEY")
embeddingModel = OpenAIEmbeddings(model="text-embedding-3-small", api_key=apiKey)

FAISS_STORE = "./store/vectorDbFaissOpenAI"

def getFaissReteriever(chunks):
    if not chunks:
        raise ValueError("chunks required for FAISS")

    if not os.path.exists(FAISS_STORE):
         vDB = FAISS.from_documents(chunks, embeddingModel)
         vDB.save_local(FAISS_STORE)
    else:
         vDB = FAISS.load_local(
              FAISS_STORE,
              embeddings=embeddingModel,
              allow_dangerous_deserialization=True
              )
        
    return vDB.as_retriever(search_kwargs={"k": 10})
