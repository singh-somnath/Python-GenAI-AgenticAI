import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template(
    "You are an helping assistant. Please provide answer professionally.\n"
    "User Input : {userMessage}"
    
)

promptChain = prompt | base_llm | parser

def chatAPP():
    print("--Chat App")
    print("Enter exit for exit.")
    while True:
        userInput = input("User:")
        if userInput.lower() == "exit":
            break

        response = promptChain.invoke({"userMessage":userInput})

        print("Assistant:")
        print(response)

    print("---End---") 



