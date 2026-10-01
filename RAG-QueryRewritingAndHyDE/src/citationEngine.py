from sentence_transformers import cross_encoder
from langchain_core.documents import Document
import spacy
import numpy as np
from scipy.special import softmax
import re

modelNLI = cross_encoder.CrossEncoder(model_name_or_path="cross-encoder/nli-MiniLM2-L6-H768",
                           device="cpu")

def citation(draftAnswer:str,originalDocs : list[Document]):
    try:

        nlp = spacy.load("en_core_web_sm")        
        doc = nlp(draftAnswer)

        claims = [s.text for s in list(doc.sents) if s.text.strip()]   
        results=[]

        for claimID,claim in enumerate(claims):
            
            pairs =[(re.sub(r"\s+"," ",doc[0].page_content),claim) for doc in originalDocs]
           
            scores = modelNLI.predict(pairs,batch_size=32, convert_to_numpy=True)
            
            probabilities = softmax(scores, axis=1)

            # Entailment is index 1
            entailment_scores = probabilities[:, 1]
            
            # Best supporting chunk
            bestIndex = np.argmax(entailment_scores)

            bestScore = entailment_scores[bestIndex]

            bestDoc = originalDocs[bestIndex]

            results.append({
                "claimID": claimID,
                "claim": claim,
                "chunkID": bestDoc[0].metadata["chunkID"],
                "entailmentScore": float(bestScore),
                "document": bestDoc[0].page_content
            })

        return results
    except Exception as e:
        print(e)
        raise e



    