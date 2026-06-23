import os
from src.vector_store import VectorDBManager
from src.embedding import EmbeddingManager
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

class RAGSearch:
    def __init__(self,vectorStore: VectorDBManager, embeddingMaanger:EmbeddingManager):
        self.vectorStore = vectorStore
        self.embeddingMaanger = embeddingMaanger

    def rag_retierever(self,query:str):

        queryEmbedding = self.embeddingMaanger.get_embedding([query])[0]
        
        qresult = self.vectorStore.collection.query(
            query_embeddings=queryEmbedding,
            n_results=5
        )
        """
        format of Query Result 
        result = {
            "ids": [...],         # Unique chunk IDs
            "documents": [...],   # Document page_content details
            "metadatas": [...],   # Document Metadata details
            "distances": [...]    # Match score
        }
        """
        retireved_docs=[]
        if qresult['documents'] and qresult['documents'][0]:
            for i,(id,doc,distance,metadata) in enumerate(zip(qresult['ids'][0],qresult['documents'][0],qresult["distances"][0],qresult['metadatas'])):
                simllarity_score= 1- distance
                if simllarity_score > 0.3:
                    retireved_docs.append({
                        "id":id,
                        "content":doc,
                        "distance" : distance,
                        "metadata" : metadata,
                        "similarity-score": simllarity_score
                    })

        return retireved_docs     
    
    def rag_simple(self,query):
        load_dotenv()
        llm = ChatOpenAI(model="gpt-4o-mini",api_key= os.getenv("OPENAI_API_KEY"))

        results = self.rag_retierever(query)
        context = "\n\n".join([doc["content"] for doc in results]) if results else ""

        message = [
        {
            "role":"system",
            "content":f"""You are an assistant,answer only from the supplied contecxt"""},
        {
            "role":"user","content":f"""
            context:{context}
            Question:{query}       
        """}
        ]
        return llm.invoke(message).content
       
    






        