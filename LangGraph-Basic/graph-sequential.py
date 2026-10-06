from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List

class AgentState(TypedDict):
    name:str
    city:str
    rent:float
    rentType:str

def basicDetails(state:AgentState) -> AgentState:
     if state['city'].lower() in ["mumbai","kolkata","delhi","chennai"]:
          state['rent'] = 45000.99
     else:
          state['rent'] = 30000.00

     return state

def getRentType(state:AgentState) -> AgentState:
     if state["rent"] > 30000.00:
          state["rentType"] = "Premium"
     else:
          state["rentType"] = "Standard"

     return state

def main():
    graph = StateGraph(AgentState)
    graph.add_node("basic",basicDetails)
    graph.add_node("rentType",getRentType)

    graph.add_edge(START,"basic")
    graph.add_edge("basic","rentType")
    graph.add_edge("rentType",END)

    app= graph.compile()

    result = app.invoke({"name":"somnath","city":"kolkata"})
    print(result)


if __name__ == "__main__":
     main()


    