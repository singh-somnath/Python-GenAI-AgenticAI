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
    "Act as a helping assistant and give answer professionally.\n"
    "History : {history}\n"
    "User Message : {userMessage}"
)

promptChain = prompt | base_llm | parser

store={}
def get_sessionHistory(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
   
    print("###################################################")
    history = store[session_id]
    print(f"$$$$Length : {len(history.messages)}")
    print(history.messages)
    if len(history.messages) > 5:
        promptSummary = ChatPromptTemplate.from_template(
            "Please summerize the below conversation in 2-3 line.\n"
            "Conversation : {conversation}"
        )

        promptSummaryChain = promptSummary|base_llm | parser

        conversationMsg = history.messages[:5]
        response = promptSummaryChain.invoke({"conversation":conversationMsg})

        store[session_id] = InMemoryChatMessageHistory()
        store[session_id].add_ai_message(f"Conversation Summary : {response}")
        print("******************************************************")
        print(response)
        print("******************************************************")
    print("###################################################")
    return store[session_id]


mesageRunnable = RunnableWithMessageHistory(
    promptChain,
    get_sessionHistory,
    input_messages_key="userMessage",
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

        response = mesageRunnable.invoke({"userMessage":userInput},config={"configurable":{"session_id":session_id}})

        print("Assistant:")
        print(response)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(f"$$$$Length : {len(get_sessionHistory(session_id).messages)}")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    print("---End---") 