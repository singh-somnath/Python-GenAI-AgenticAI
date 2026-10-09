from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Sequence,List,Annotated
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import math

@tool
def addition(nums:List[float]):
    """This tool add list of numbers and return the result"""
    print("addition tool===")
    return sum(nums)

@tool
def multiplication(nums:List[float]):
      """This tool multiply list of numbers and return the result"""
      print("muriplication tool===")
      return math.prod(nums)

class AgentState(TypedDict):
     messages : Annotated[Sequence[BaseMessage],add_messages]
     apikey :str
     llm:ChatOpenAI
     model:str


def setup(state:AgentState)->AgentState:
     load_dotenv()
     tools=[addition,multiplication]
     state['apikey'] = os.getenv("OPENAI_API_KEY")
     state['model'] = "gpt-4o-mini"
     state['llm'] = ChatOpenAI(model=state['model'],api_key=state['apikey']).bind_tools(tools=tools)
     state['messages'] = []

     return state

def model_call(state:AgentState) -> AgentState:
    response = state['llm'].invoke(state['messages'])
    if response.content:
        print("===Agent===")
        print(response.content) 
    return {
         'messages' : [response]
         }

def shouldContinue(state:AgentState):
     response = state["messages"][-1]   
     if  response.tool_calls:        
          return "tools"
     else:         
          return "end"

def main():
     graph = StateGraph(AgentState)

     graph.add_node("setup",setup)
     graph.add_node("llm",model_call)

     tools=[addition,multiplication]
     graph.add_node("tools",ToolNode(tools=tools))

     

     graph.add_edge(START,"setup")
     graph.add_edge("setup","llm")
     graph.add_conditional_edges(
          "llm",
          shouldContinue,
          {
               "tools":"tools",
               "end":END
          }
     )
     graph.add_edge("tools","llm")

     app = graph.compile()

     user_input = input("Enter your query [enter exit for exit] : ")
     app.invoke({'messages':[HumanMessage(content=user_input)]})


          
     
if __name__=="__main__":
     main()
