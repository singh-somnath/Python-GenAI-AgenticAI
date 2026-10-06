from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List


class AgentState(TypedDict):
    name:str
    age:int
    skills:List[str]
    result:str

def firstNode(state:AgentState) -> AgentState:
    state['result'] = f"{state['name']} , welcome to the system!"

    return state

def secondNode(state:AgentState) -> AgentState:
    state['result'] = state['result'] + f" You are {state['age']} years old! "
    return state

def thirdNode(state:AgentState)->AgentState:
    state['result'] = state['result'] + f"You have skills in : {",".join(state['skills'])}"
    return state

def main():
    graph = StateGraph(AgentState)

    graph.add_node("first",firstNode)
    graph.add_node("second",secondNode)
    graph.add_node("third",thirdNode)

    graph.add_edge(START,"first")
    graph.add_edge("first","second")
    graph.add_edge("second","third")
    graph.add_edge("third",END)

    app = graph.compile()

    result = app.invoke({'name':"somnath","age":36,"skills":["Python","AI","SharePoiunt O365"]})
    print(result['result'])


if __name__=="__main__":
    main()