from sentence_transformers import cross_encoder
from langchain_core.documents import Document
import spacy
import numpy as np
from scipy.special import softmax
import re

modelNLI = cross_encoder.CrossEncoder(
            model_name_or_path="cross-encoder/nli-MiniLM2-L6-H768",
            device="cpu"
        )

def citation(userQuery:str,draftAnswer:str,originalDocs : list[Document]):
    try:

        nlp = spacy.load("en_core_web_sm")        
        doc = nlp(draftAnswer)

        claims = [s.text for s in list(doc.sents) if s.text.strip()]   
        citations=[]
        unsupported = []


        for claimID,claim in enumerate(claims,start=1):
            
            pairs =[(re.sub(r"\s+"," ",doc.page_content),claim) for doc in originalDocs]
           
            scores = modelNLI.predict(pairs,batch_size=32, convert_to_numpy=True)
            
            probabilities = softmax(scores, axis=1)

            # Entailment is index 1
            entailment_scores = probabilities[:, 1]

            # Best supporting chunk
            bestEntailmentIndex = np.argmax(entailment_scores)

            bbestEntailmentScore = probabilities[bestEntailmentIndex][1]
            bestContradictionScore = probabilities[bestEntailmentIndex][0]
            bestNeutralScore = probabilities[bestEntailmentIndex][2]

            if bbestEntailmentScore >= 0.75 and bbestEntailmentScore > bestContradictionScore:
                bestDoc = originalDocs[bestEntailmentIndex]

                citations.append({
                    "claimID": claimID,
                    "claim": claim,
                    "status":"supported",
                    "chunkID": bestDoc.metadata["chunkID"],
                    "entailmentScore": float(bbestEntailmentScore),
                    "maxContradictionScore" : float(bestContradictionScore),
                    "document": bestDoc
                })

                print(f'[NLI] Chunk ID :{bestDoc.metadata["chunkID"]} | Status : Supported | Entailment Score : {float(bbestEntailmentScore)} | Contradict Score : {float(bestContradictionScore)} ')
            else:
                unsupported.append({
                    "claimID": claimID,
                    "claim": claim,
                    "status":"unsupported",
                    "entailmentScore": float(bbestEntailmentScore),
                    "maxContradictionScore" : float(bestContradictionScore)
                })
                print(f'[NLI] Claim :{claim[:100]} | Status : Unsupported | Entailment Score : {float(bbestEntailmentScore)} | Contradict Score : {float(bestContradictionScore)} ')

        return citations,unsupported
    except Exception as e:
        print(e)
        raise e



    