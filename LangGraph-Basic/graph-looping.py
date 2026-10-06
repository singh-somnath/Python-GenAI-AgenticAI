from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):
    name : str
    result : str
    counter: int


def greet(state:AgentState)->AgentState:
    state['counter'] = state['counter'] + 1
    state['result'] = state['result'] + f"{state['counter']} - Hi {state['name']} , Welcome to the system\n"
   
    return state

def loopingLogic(state:AgentState):
    if state['counter'] < 50:
        return "continue"
    else:
        return "end"

def main():
    graph = StateGraph(AgentState)

    graph.add_node("greet",greet)
    
    graph.add_edge(START,"greet")

    graph.add_conditional_edges(
        "greet",
        loopingLogic,
        {
            "continue":"greet",
            "end" : END
        }
    )

    app = graph.compile()

    result = app.invoke({"name":"somnath", 'result':"", "counter":0})

    print(result["result"])


if __name__=="__main__":
    main()