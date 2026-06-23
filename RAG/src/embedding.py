import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.data_loader import load_all_documents

class EmbeddingManager:
    def __init__(self):
        self.modal =SentenceTransformer("all-MiniLM-L6-v2") 

    def get_chunks(self,data_dir:str):
        allDocs = load_all_documents(data_dir)

        doc_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 80,
            length_function = len
        )
        return doc_splitter.split_documents([doc for doc in allDocs])
    
    def get_embedding(self, text:list[str]) -> np.ndarray:
          return self.modal.encode(text)
        

