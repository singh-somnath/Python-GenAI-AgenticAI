from langgraph.graph import StateGraph, START, END
from typing import TypedDict,List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",api_key=apikey)

class AgentState(TypedDict):
    messages : List[HumanMessage]  


def chatNode(state:AgentState) -> AgentState:
    
    print(state["messages"])
    print("**********************************************************")
    response = llm.invoke(state["messages"])
    print("==== Agent ========")
    print(response.content)  

    return state

def main():
    graph = StateGraph(AgentState)

    graph.add_node("chatnode",chatNode)

    graph.add_edge(START,"chatnode")
    graph.add_edge("chatnode",END)

    app = graph.compile()

    user_input = input("Enter your query [enter exit for exit] : ")
    while user_input.lower() != "exit":      
        app.invoke({'messages':[HumanMessage(content=user_input)]})
        user_input = input("Enter your query [enter exit for exit] : ")


if __name__=="__main__":
    main()

       

