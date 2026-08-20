import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template(
    "You are an helping assistant. Please give naswer professioanlly\n"
    "Message History : {history}"
    "User Message : {input}"
)

promptChain = prompt | base_llm | parser

store = {}

def get_sessionHistory(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chatRunnable = RunnableWithMessageHistory(
    promptChain,
    get_sessionHistory,
    input_messages_key="input",
    history_messages_key="history"
)

session_id = "user123"

def chatAPP():
    print("--Chat App")
    print("Enter exit for exit.")
    while True:
        userInput = input("User:")
        if userInput.lower() == "exit":
            break

        response = chatRunnable.invoke({"input":userInput},config={"configurable":{"session_id":session_id}})

        print("Assistant:")
        print(response)

    print("---End---") 
