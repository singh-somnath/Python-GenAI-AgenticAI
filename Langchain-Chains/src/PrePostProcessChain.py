import os
import json
from datetime import datetime
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch, RunnableLambda

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

#Preprocessing
def preprocessingText(inputText:str):
    inputText = inputText.strip()
    inputText = re.sub(r"\s+"," ",inputText)
    inputText=re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b','[EMAIL_MASKED]',inputText)
    inputText = inputText.replace("pls","Please").replace("thx","Thanks")
    return inputText

preProcessing = RunnableLambda(preprocessingText)

prompt = PromptTemplate(
    input_variables=["cleanText"],
    template=""""
        You are an helping assistant. Please ive the appropriate reply for the below clean text.\n
        Clean Text : {cleanText}
    """
)

promptChain = prompt | base_llm | parser

def postProcessingText(response:str,originalText:str):
    response = re.sub(r"\n\n","\n",response)
    jsonText = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "response" : response,
        "original-text":originalText,
        "total-words":len(response.strip())
    }
    return json.dumps(jsonText,indent=4)

postProcessing = RunnableLambda(lambda output : postProcessingText(output["response"],output["input"]))

def processMessage(inputText):
    cleanText = preProcessing.invoke(inputText)
    response = promptChain.invoke({"cleanText":cleanText})
    postResponse = postProcessing.invoke({"response":response,"input":cleanText})
    return postResponse

messages=[
"I contacted john.smith@example.com regarding my login issue three days ago, but I have not received any response yet.",
"Despite multiple follow-ups to sarah.jones@example.com, the issue with the missing accessories has not been resolved.",
"I reported frequent internet disconnections to michael.brown@example.com, but the problem still persists.",
"I emailed emily.davis@example.com about the duplicate charge on my account, but my refund request remains pending.",
"The incorrect leave balance issue was reported to robert.wilson@example.com, however I am still unable to submit my leave request."
]

def messageResponse(index:int):
    message = messages[index]
    response = processMessage(message)
    print(response)
    jsonRes = json.loads(response)
    print(jsonRes["response"])
