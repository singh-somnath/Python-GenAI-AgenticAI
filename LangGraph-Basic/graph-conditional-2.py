from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    number1:float
    number2:float
    operation1:str
    number3:float
    number4:float
    operation2:str
    finalNumber1:float
    finalNumber2:float

def addition1(state:AgentState)->AgentState:
    state['finalNumber1'] = state['number1'] + state['number2']
    return state

def addition2(state:AgentState)->AgentState:
    state['finalNumber2'] = state['number3'] + state['number4']
    return state

def subtract1(state:AgentState)->AgentState:
    state['finalNumber1'] = state['number1'] - state['number2']
    return state

def subtract2(state:AgentState)->AgentState:
    state['finalNumber2'] = state['number3'] - state['number4']
    return state

def rputeOperation1(state:AgentState):
    if state['operation1'] == "+":
        return "add"
    else:
        return "subtract"

def rputeOperation2(state:AgentState):
    if state['operation2'] == "+":
        return "add"
    else:
        return "subtract"


def main():
    graph= StateGraph(AgentState)

    graph.add_node("add1",addition1)
    graph.add_node("subtract1",subtract1)
    graph.add_node("add2",addition2)
    graph.add_node("subtract2",subtract2)
    graph.add_node("router1",lambda s : s)
    graph.add_node("router2",lambda s : s)

    graph.add_edge(START,"router1")
    graph.add_conditional_edges(
        "router1",
        rputeOperation1,
        {
            "add":"add1",
            "subtract":"subtract1"
        }

    )
    graph.add_edge("add1","router2")
    graph.add_edge("subtract1","router2")
    graph.add_conditional_edges(
            "router2",
            rputeOperation2,
            {
                "add":"add2",
                "subtract":"subtract2"
            }
    
    )
    graph.add_edge("add2",END)
    graph.add_edge("subtract2",END)

    app = graph.compile()

    result = app.invoke({'number1':10,'number2':20,"operation1":"+",'number3':140,"number4":50,"operation2":"-"})
    print(result)

if __name__=="__main__":
    main()