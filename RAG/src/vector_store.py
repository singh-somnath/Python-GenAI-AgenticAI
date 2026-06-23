import os
import chromadb
from uuid import uuid4

class VectorDBManager:

    def __init__(self):
        os.makedirs("./data/vaector-chromadb",exist_ok=True)
        self.client = chromadb.PersistentClient(path="../data/vaector-chromadb")
        self.collection = self.client.get_or_create_collection(name="documents",metadata={"description":"This vector db used for all documents"})

    def add_documents(self,documents,embeddings):

        idList=[]
        metadataList=[]
        documentList=[]
        embeddingList =[]

        for i,(document,embedding) in enumerate(zip(documents,embeddings)):
                id = f"doc_id_{i}_{uuid4().hex[:8]}" 
                idList.append(id)
                
                metadata = document.metadata
                metadata["doc_index"] = i
                metadata["content_length"] = len(document.page_content)
                metadataList.append(metadata)

                documentList.append(document.page_content)
                embeddingList.append(embedding.tolist())           
        
        self.collection.add(
             ids=idList,
             metadatas= metadataList,
             documents= documentList,
             embeddings=embeddingList
        )