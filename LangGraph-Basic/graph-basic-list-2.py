from langgraph.graph import StateGraph,START,END
from typing import List,TypedDict
import math

class AgentState(TypedDict):
    name:str
    num:List[int]
    operation:str
    result:str


def process(state:AgentState)->AgentState:
    if state['operation'] == "+":
        state['result'] = f"Hi {state['name']}, sum of numbers : {str(sum(state['num']))}." 
    elif state['operation'] == "*":
        state['result'] = f"Hi {state['name']}, multiplication of numbers : {str(math.prod(state['num']))}."


    return state

def main():

    graph = StateGraph(AgentState)

    graph.add_node("process",process)
    graph.add_edge(START,"process")
    graph.add_edge("process",END)

    app = graph.compile()

    result = app.invoke({'name' : "somnath",'operation':"+", 'num' : [8,7,3,2,4] })
    print(result['result'])


if __name__ == "__main__":
    main()