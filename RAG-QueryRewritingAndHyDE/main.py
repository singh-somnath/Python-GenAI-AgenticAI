from dotenv import load_dotenv
load_dotenv()
from src.reteriever_BM25 import getBM25
from src.reteriever_FAISS import getFaissReteriever
from src.loader import getDocumentsChunks
from src.multiLevelReteriver import multiLevelReteriever
from src.llmResponse import askLLM
from src.citationEngine import citation
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
import numpy as np
import re

def test():
    modelNLI = CrossEncoder(
        "cross-encoder/nli-MiniLM2-L6-H768",
        device="cpu"
    )
    text = """
    Page 7\napp.include_router(...) merges those routes into the live application — three separate, isolated\npieces assembled into one working API.\n\n3.3 Middleware & CORS\n• Middleware is code that runs on every request/response passing through the app — used for\nlogging, timing, adding custom headers, etc., via @app.middleware("http").\n• CORS (Cross-Origin Resource Sharing) is a browser security rule that blocks a webpage on one\ndomain from calling an API on a different domain, unless the API explicitly allows it.\n• FastAPI enables CORS using CORSMiddleware, configured with allow_origins, allow_methods,\nallow_headers, and allow_credentials.\n• CORS is a browser-enforced guardrail only — it doesn\'t stop direct server-to-server calls (e.g., via\ncurl/Postman), so it must always be paired with real authentication.\n\nfrom fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\nimport time\n\napp = FastAPI()\n\napp.add_middleware(\nCORSMiddleware,\nallow_origins=["https://myapp.example.com"], # never "*" with credentials\nallow_credentials=True,\nallow_methods=["GET", "POST", "PUT", "DELETE"],\nallow_headers=["Authorization", "Content-Type"],\n)\n\n@app.middleware("http")\nasync def add_process_time_header(request, call_next):\nstart = time.perf_counter()\nresponse = await call_next(request)\nresponse.headers["X-Process-Time"] = str(time.perf_counter() - start)\nreturn response\nImportant: CORS is a browser-enforced guardrail, not server-side security. It stops malicious\nwebpages from reading your API\'s response in a victim\'s browser — it does NOT stop direct\ncalls via curl/Postman/server-to-server. Always pair it with real authentication (Part 4).\n\n• Middleware handles every HTTP request and response.\n• Register using @app.middleware("http").\n• request contains incoming request data.\n• call_next continues request processing.\n• Code before call_next handles the request.\n• Code after call_next handles the response.\n• return response sends the final response.
    """
    print(len(text))
    premise = text[:700]

    hypothesis = """
    CORS (Cross-Origin Resource Sharing) in FastAPI is managed using the CORSMiddleware.
    """

    scores = modelNLI.predict(
        [(premise, hypothesis)],
        convert_to_numpy=True
    )

    print("Scores:", scores)
    print("Labels:", modelNLI.model.config.id2label)
    print("Prediction:", modelNLI.model.config.id2label[np.argmax(scores[0])])

def main():
    try:
        #chunks = getDocumentsChunks()
        #vectorStore = getReteriever(chunks)
        #docs = vectorStore.invoke(query)
        #for doc in docs:
        #    print(doc)
        #test()
        #return
        documents = getDocumentsChunks()
        
        bm25Reteriever = getBM25(documents)
        vectorReteriver = getFaissReteriever(documents)
        while True:
            print("--------------------------")
            print("--------------------------")
            inputQ =input("Enter your query [For stop enter exit] : ")

            if inputQ.lower() == "exit":
                break

           
            distilDocs = multiLevelReteriever(inputQ,bm25Reteriever,vectorReteriver,documents)
            
            contextDocs:list[str] =[]
            for doc in distilDocs:                
                contextDocs.append(doc.page_content)
                

            #print("Response : ")
            draftAnser = askLLM(inputQ,contextDocs,"user-123")
            citationResult = citation(str(draftAnser),distilDocs)
            print("Response :")
            print(draftAnser)
            print("**************************************")
            print(citationResult)
            print("***************************************")



            
        
               

        print("------------End--------------")

    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    main()
