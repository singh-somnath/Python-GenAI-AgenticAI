from rank_bm25 import BM25Okapi

from langchain_core.documents import Document

def getTokenizedCorpus(documents:list[Document]):
    return [doc.page_content.lower().split() for doc in documents]
    

def getBM25(documents:list[Document]):
    corpus = getTokenizedCorpus(documents)
    return BM25Okapi(corpus)

def getQueryForBM25(query:str):
    token = query.lower().split()
    return token


