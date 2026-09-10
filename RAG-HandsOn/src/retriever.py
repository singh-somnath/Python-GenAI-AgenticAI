from langchain_community.vectorstores import FAISS


from langchain_chroma import Chroma
import os
from dotenv import load_dotenv



load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

def basicRetriever(vectorStore : FAISS | Chroma):
   retriever =  vectorStore.as_retriever(search_kwargs={'k':3})
   return retriever


