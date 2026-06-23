from src.embedding import EmbeddingManager
from src.vector_store import VectorDBManager
from src.search import RAGSearch

if __name__ == "__main__":
    emManager = EmbeddingManager()
    splitDocs = emManager.get_chunks("./data")     
    embeddings = emManager.get_embedding([doc.page_content for doc in splitDocs])

    vManager = VectorDBManager()
    vManager.add_documents(splitDocs,embeddings)

    ragSearch = RAGSearch(vManager,emManager)
    result = ragSearch.rag_simple("Give details about maternity leave")
    print(result)