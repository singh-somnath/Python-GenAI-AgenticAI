from langchain_community.embeddings import SentenceTransformerEmbeddings  
from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")

def getEmbedding(type="Local"):
    if type.lower() == "local":
        embedding = SentenceTransformerEmbeddings(
            model_name = "all-MiniLM-L6-v2"
        )
        return embedding
    else:
        embedding = OpenAIEmbeddings(
            model = "text-embedding-3-small",
            api_key=apikey
        )
        return embedding

