from src.reteriever_BM25 import getBM25, getQueryForBM25
from src.reteriever_FAISS import getFaissReteriever
from src.loader import getDocumentsChunks
import numpy as np
from collections import defaultdict

def reciprocal_rank_fusion(result_list,k=60):
    scores=defaultdict(float)
    docs = {}

    for result in result_list:
        for rank,doc in enumerate(result,start=1):
            currentDocID = doc.metadata["chunkID"]

            scores[currentDocID] += 1/(k+rank)
            docs[currentDocID] = doc

    print(scores)

    ranked =  sorted(
        scores.items(),
        key = lambda x : x[1],
        reverse=True
    )
    print(ranked)




def multiLevelReteriever(query:str):
    documents = getDocumentsChunks()

    bm25Reteriever = getBM25(documents)
    vectorReteriver = getFaissReteriever(documents)

    vDocs = vectorReteriver.invoke(query)

    print("VDb Docs : ")
    for doc in vDocs:
        print(doc.metadata["chunkID"])

    queryBM25 = getQueryForBM25(query)
    bm25Scores = bm25Reteriever.get_scores(queryBM25)


    bestDOCIDX = np.argsort(bm25Scores)[::-1][:5]

    resultBM25=[]


    print("BM25 Docs : ")
    for id in bestDOCIDX:
        doc = documents[id]
        print(doc.metadata["chunkID"])
        doc.metadata["scoreBM25"] = bm25Scores[id]
        resultBM25.append(doc)

    reciprocal_rank_fusion([vDocs,resultBM25])
