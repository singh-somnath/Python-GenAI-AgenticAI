from rank_bm25 import BM25Okapi

from langchain_core.documents import Document

bm25:BM25Okapi = None

def getTokenizedCorpus(documents:list[Document]):
    return [doc.page_content.lower().split() for doc in documents]
    

def getBM25(documents:list[Document]):
    global bm25

    if bm25 is None:
        corpus = getTokenizedCorpus(documents)
        bm25 = BM25Okapi(corpus)

    return bm25

def getQueryForBM25(query:str):
    token = query.lower().split()
    return token


