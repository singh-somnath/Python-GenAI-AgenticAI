from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START,END
from typing import TypedDict,List
from langchain_core.messages import HumanMessage, AIMessage



class AgetState(TypedDict):
    messgaes : List[HumanMessage|AIMessage]
    userQuery : str
    apikey : str
    llm : ChatOpenAI

def setup(state:AgetState) ->  AgetState:
    print("setup started...")
    load_dotenv()
    state['apikey'] = os.getenv("OPENAI_API_KEY")
    state['llm'] = ChatOpenAI(model="gpt-4o-mini",api_key=state['apikey'])
    state['messgaes'] = []

    return state


def chatNode(state:AgetState) -> AgetState:
     print("chat started...")
     user_input = state['userQuery']
     while user_input.lower() != "exit": 
            state['messgaes'].append(HumanMessage(content=user_input))
            print(state["messgaes"])
            response = state['llm'].invoke(state['messgaes'])
            print("====Agent====")
            print(response.content)           
            state['messgaes'].append(AIMessage(content=response.content))
            user_input = input("Enter your query [enter exit for exit] : ")
    

     return state

def main():
    graph = StateGraph(AgetState)

    graph.add_node("setup",setup)
    graph.add_node("chat",chatNode)

    graph.add_edge(START,"setup")
    graph.add_edge("setup","chat")
    graph.add_edge("chat",END)

    app = graph.compile()

    user_input = input("Enter your query [enter exit for exit] : ")
    app.invoke({'userQuery':user_input})         
            
    
if __name__=="__main__":
    main()