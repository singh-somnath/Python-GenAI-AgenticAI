import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

complaints=[
"The text on one of the buttons is slightly misaligned. It still works, but it doesn’t look right.",
"I have to click twice to close the notification pop-up sometimes.",
"The exported report shows the date in a different format than what I selected.",
"I’m occasionally unable to log in and have to refresh the page several times before it works.",
"The application has become extremely slow during peak hours, and it is affecting our daily work.",
"Some transaction totals in the dashboard don’t match the figures in our source system.",
"The reporting feature has stopped working for our team, although the rest of the application is accessible.",
"Our entire production system is down, and none of our users can access the application.",
"Customer transactions are being charged twice, resulting in incorrect financial deductions.",
"A user can see information belonging to another customer, which appears to be a serious data privacy issue."
]

summary_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
    Give a summary of this complaint from customer \n
    complaint : {message} 
    """
)

summaryChain = summary_prompt | base_llm | parser

severity_prompt = PromptTemplate(
    input_variables=["summary"],
    template="""
    Get the exact severity from the below summary and give it only in one word either any one of these - High, Low, Medium.\n
    Summary : {summary} 
    """
)
severityChain = severity_prompt | base_llm | parser

response_prompt = PromptTemplate(
    input_variables=["summary","severity"],
    template=""""
    Please provide the auto response beased on the below summary and severity. If severity is low or medium theny only provide auto respone.\n
    If severity is high the redirect the complaint to the support team immediatly.\n
    Summary : {summary}\n
    Severity : {severity}

    """
)

responseChain = response_prompt | base_llm | parser

def complaintHybridResponse(index:int):
    currentComplaint = complaints[index]
    print("Complaint")
    print(currentComplaint)
    print("Summary")
    summary = summaryChain.invoke({"message":currentComplaint})
    print(summary)
    print("Severity")
    severity = severityChain.invoke({"summary":summary})
    print(severity)
    print("Response")
    response = responseChain.invoke({"summary":summary,"severity":severity})
    print(response)