from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    number1:int
    number2:int
    operation:str
    result:str

def addition(state:AgentState) -> AgentState:
    state['result'] = state['number1'] + state['number2']
    return state

def substraction(state:AgentState) -> AgentState:
    state['result'] = state['number1'] - state['number2']
    return state

def routeOperation(state:AgentState):
    if state["operation"] == "+":
        return "add"
    else:
        return "substracte"

def main():
    graph = StateGraph(AgentState)

    graph.add_node("addition",addition)
    graph.add_node("substraction",substraction)
    graph.add_node("router",lambda state:state)

    graph.add_edge(START,"router")

    graph.add_conditional_edges(
        "router",
        routeOperation,{
            "add":"addition",
            "substracte":"substraction"
        }
    )

    graph.add_edge("addition",END)
    graph.add_edge("substraction",END)

    app = graph.compile()

    result = app.invoke({'number1':1289,"number2":123,"operation":"+"})
    print(result["result"])


if __name__=="__main__":
    main()