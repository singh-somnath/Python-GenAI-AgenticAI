from src.loader import textDocLoader,pdfDocLoader,bsHtmlFileLoader,unsturucteredUrlLoader
from src.chunking import getChunksUsingRecursiveSplitter
from src.ebmedding import getEmbedding
from src.vectorStore import initiallizeVectorDB, getVectorDB
from src.retriever import basicRetriever
from src.load import rag_chain

def main():
    print("Hello from rag-handson!")

def initialize():
    docs = []
    docs.extend(textDocLoader())
    #docs.extend(pdfDocLoader())
    #docs.extend(bsHtmlFileLoader())
    #docs.extend(unsturucteredUrlLoader())

    chunks = getChunksUsingRecursiveSplitter(docs)
    embedding_model = getEmbedding("Local")    
    initiallizeVectorDB(chunks,embedding_model)

def searchWithChroma(query):
    embedding_model = getEmbedding("Local")
    db = getVectorDB(embedding_model,type="chroma")
    retriever = basicRetriever(db)
    return retriever.invoke(query)
basicRetriever
def searchWithFAISS(query):
    response = rag_chain().invoke({"question":query})
    print(response)

    


if __name__ == "__main__":
   searchWithFAISS("What Are the Main Types of Machine Learning?")

