from langgraph.graph import StateGraph, START, END
from typing import TypedDict,List
import random

class AgentState(TypedDict):
    playerName:str
    guesses:List[int]
    targetNumber:int
    attepts:int
    lowerBound:int
    upperBound:int
    counter:int

def setup(state:AgentState)->AgentState:
    state['attepts'] = 0
    state['lowerBound'] = 1
    state['upperBound'] = 20
    state['guesses'] = []
    print(f"Welcome {state['playerName']}")
    print(f"I am started guseesing. (Target Number - {state['targetNumber']})")

    return state


def guess(state:AgentState) ->AgentState:
    state['attepts'] = state['attepts'] + 1
    possibleGuesses = [i for i in range(state['lowerBound'],state['upperBound']) if i not in state['guesses']]
    guess = random.choice(possibleGuesses)
    state['guesses'].append(guess)
    print(f"[{state['attepts']}] Guess : {guess} ")

    return state

def should_continue(state:AgentState):

    guessedNumber = state['guesses'][-1]

    if guessedNumber == state['targetNumber']:
        print(f"Guess tak completed sucessfully-")
        print(f"Total attempts - {state['attepts']}")
        return "end"
    elif state['attepts'] >= 7:
        print(f"Tried 7 times. Task completed without guessing the target number [{state['targetNumber']}]")
        return "end"
    else:
        return "continue"

def guess_hint(state:AgentState) -> AgentState:
   
    guessedNumber = state['guesses'][-1]    

    if guessedNumber < state['targetNumber']:
        state['lowerBound'] = guessedNumber
    elif guessedNumber > state['targetNumber']:
        state['upperBound'] = guessedNumber

    return state

def main():
    graph = StateGraph(AgentState)

    graph.add_node("setup",setup)
    graph.add_node("guess",guess)
    graph.add_node("hint",guess_hint)

    graph.add_edge(START,"setup")
    graph.add_edge("setup","guess")
    graph.add_conditional_edges(
        "guess",
        should_continue,
        {
            "continue":"guess",
            "end":END
        }
    )

    app = graph.compile()
    app.invoke({'playerName':'somnath','targetNumber':4})


if __name__=="__main__":
    main()






