from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List

class AgentState(TypedDict):
    num:List[int]
    name:str
    result:str


def process(state:AgentState)->AgentState:
    """It is adding list of numbers"""
    state['result'] = "Hi " + state['name']  + ", sum of numbers : " + str(sum(state['num'])) + "."

    return state


def main():
    graph = StateGraph(AgentState)

    graph.add_node("process",process)
    graph.add_edge(START,"process")
    graph.add_edge("process",END)

    app = graph.compile()

    result = app.invoke({"name":"Som","num":[2,3,4,5,6,7]})

    print(result["result"])


if __name__=="__main__":
    main()
