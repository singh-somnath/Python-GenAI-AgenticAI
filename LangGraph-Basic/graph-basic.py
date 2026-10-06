from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message:str


def firstNode(state:AgentState)->AgentState:
    """Simple node that add messages"""
    state['message'] = "Hi " + state['message'] + ", How are you?"
    return state



def main():
    graph = StateGraph(AgentState)

    graph.add_node("firstNode",firstNode)

    graph.set_entry_point("firstNode")
    graph.set_finish_point("firstNode")

    app = graph.compile()

    content = app.invoke({"message":"Ram"})

    print(content["message"])

if __name__ == "__main__":
    main()