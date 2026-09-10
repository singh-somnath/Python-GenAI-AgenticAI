from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from src.loader import textDocLoader

def getChunksUsingRecursiveSplitter(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap=150
    )
    return splitter.split_documents([doc for doc in documents])


def getChunksUsingTokenSplitter(documents):
    splitter = TokenTextSplitter(
        chunk_size = 80,
        chunk_overlap = 30
    )

    return splitter.split_documents([doc for doc in documents])
