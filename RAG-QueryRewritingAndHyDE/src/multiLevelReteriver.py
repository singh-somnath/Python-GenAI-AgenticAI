from sentence_transformers import cross_encoder
import spacy
from src.reteriever_BM25 import getQueryForBM25
import numpy as np
from collections import defaultdict
from rank_bm25 import BM25Okapi
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
import re

def distilation(query:str, docs:list[Document]):
    try:
        model = cross_encoder.CrossEncoder(
            model_name_or_path = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            device="cpu"
        )

        distilarDocs : list[Document] =[]
        nlp = spacy.load("en_core_web_sm")   
        
        for doc in docs:
            
            content = doc[0].page_content
                 
            corpus = nlp(content)
            sentences = [sentence.text for sentence in list(corpus.sents) if sentence.text.strip()]

            pairs = [(query,sentence) for sentence in sentences]

            scores = model.predict(pairs,batch_size=32)

            ranked = sorted(
                [(index,sentence,score) for index,(sentence,score) in enumerate(zip(sentences,scores))],
                key = lambda x : x[2],
                reverse= True 
            )[:3]

            sortedRanked = sorted(
                ranked,
                key = lambda x: x[0],
                reverse= False
            )

            compressedContent = "\n".join([sentence for _,sentence,_ in sortedRanked])

            distilatedDoc = Document(
                page_content=compressedContent,
                metadata = doc[0].metadata.copy()
            )
            distilarDocs.append(distilatedDoc)

        
        return distilarDocs
    except Exception as e:
        print(e)
        raise e

        


def applyCroossEncoder(query:str, docs:list[Document]):
    model = cross_encoder.CrossEncoder(
        model_name_or_path = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device="cpu"
    )

    pairs =[(query,doc.page_content) for doc,_ in docs]

    scores = model.predict(pairs, batch_size=32)

    ranked = sorted(
        zip(docs,scores),
        key = lambda x : x[1],
        reverse= True 
    )   

    return distilation(query,[ doc for doc,_ in ranked[:5]])

    

def reciprocal_rank_fusion(query,result_list,k=60):
    scores=defaultdict(float)
    docs = {}

    for result in result_list:
        for rank,doc in enumerate(result,start=1):
            currentDocID = doc.metadata["chunkID"]

            scores[currentDocID] += 1/(k+rank)
            docs[currentDocID] = doc
  

    ranked =  sorted(
        scores.items(),
        key = lambda x : x[1],
        reverse=True
    )

    rankedDocs = [(docs[docid],score) for docid,score in ranked]    

    return applyCroossEncoder(query,rankedDocs) 
    

def multiLevelReteriever(query:str,bm25Reteriever:BM25Okapi,vectorReteriver:VectorStoreRetriever,documents:list[Document]):
  

    vDocs = vectorReteriver.invoke(query)
   
    for doc in vDocs:
        doc.metadata["source"] = "Vector DB"      

    queryBM25 = getQueryForBM25(query)
    bm25Scores = bm25Reteriever.get_scores(queryBM25)


    bestDOCIDX = np.argsort(bm25Scores)[::-1][:10]

    resultBM25=[]

   
    for id in bestDOCIDX:
        doc = documents[id]
        doc.metadata["scoreBM25"] = bm25Scores[id]
        doc.metadata["source"] = "BM25"    
      
        resultBM25.append(doc)
 

    multiReterieverResults =[vDocs,resultBM25]

    return reciprocal_rank_fusion(query,multiReterieverResults)
