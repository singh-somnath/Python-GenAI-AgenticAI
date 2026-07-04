"""
Middleware provides a way to more tightly control what happens inside the agent. Middleware is useful for the following:
        -Tracking agent behavior with logging, analytics, and debugging.
        -Transforming prompts, tool selection, and output formatting.
        -Adding retries, fallbacks, and early termination logic.
        -Applying rate limits, guardrails, and PII detection.

InMemorySaver
        -Stores the agent's conversation state (messages, summaries, etc.) between invocations.
        -Acts as the memory backend for the agent.
        -Configured when the agent is created.
        -Memory exists only while the application is running; it is lost if the process restarts.

thread_id
        -Uniquely identifies a conversation.
        -Tells the checkpointer which conversation's state to load and update.
        -Passed in the config during each agent.invoke() call.
        -Enables multiple independent conversations to share the same checkpointer without mixing their histories.

InMemorySaver = the filing cabinet that stores conversation files.
thread_id = the label on a folder that identifies which conversation to retrieve and update.


Summarization Middleware automatically manages an agent's memory by replacing older conversation history 
with a concise summary before context limits are reached. It can be triggered by:
    -Message count (trigger=("messages", N))
    -Token count (trigger=("tokens", N))
    -Fraction of the model's context window (trigger=("fraction", 0.85))
"""

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware,HumanInTheLoopMiddleware
from langgraph.types import Command
from langchain_openai import ChatOpenAI 
import os
from dotenv import load_dotenv
from rich import print

def agent_SummarizationMiddleware():
    load_dotenv()
    os.getenv("OPENAI_API_KEY")

    agent = create_agent(
        model="gpt-4o-mini",
        tools=[],
        checkpointer=InMemorySaver(),
        middleware=[SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("messages",10),
            keep=("messages",4)
        )]
    )

    configuration_t1 = {"configurable":{"thread_id":"thread_1"}}
    configuration_t2 = {"configurable":{"thread_id":"thread_2"}}

    counter = 1
    while True:
        user_input = input("\nUser [Tpye exit for quit Converstaion]: ")

        if user_input.lower() in ["exit"]:
            break
        
        response = agent.invoke({"messages":[HumanMessage(content=user_input)]},configuration_t1)
        print(response["messages"])
        print(f"Message Count - {len(response['messages'])}")

"""
Human In the Loop MiddleWare

Pause agent execution for human approval, editing, or rejection of tool calls before they execute. Human-in-the-loop is useful for the following:

            -High-stakes operations requiring human approval (e.g. database writes, financial transactions).
            -Compliance workflows where human oversight is mandatory.
            -Long-running conversations where human feedback guides the agent.

Key Points : 

HumanInTheLoopMiddleware → Specifies which tools require approval.
checkpointer → Required to pause and resume execution.
create_agent() → Registers the model, tools, middleware, and checkpointer.
thread_id → Identifies the execution thread for resuming.
Command(resume=...) → Continues execution after the human decision. 
    agent.invoke(Command(resume={"decisions":[{"type":user_input}]}),config=configuration)

"""

def sendMail(emailId, subject, body):
    """
    This function is responsible for sending mail with subject, bosy and to the designate emailId
    """ 
    print(f"Sending email to: {emailId}\nSubject: {subject}\nBody: {body}")


def agent_HumanInTheLoopMiddlewar():
    load_dotenv()
    os.getenv("OPENAI_API_KEY")

    agent = create_agent(
        model="gpt-4o-mini",
        tools=[sendMail],
        checkpointer=InMemorySaver(),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "sendMail":{
                        "allowed_decisions":["approve","edit","reject"]
                    }
                }
            )
        ]
    )

    configuration = {"configurable":{"thread_id":"thread_1"}}

    result = agent.invoke(input={"messages":[HumanMessage("Send mail to ss@sg.com with subject - project status and body - All task completed")]}, config= configuration)
    
    #Invalid Call - System will not allow
    #result2 = agent.invoke(input={"messages":[HumanMessage("How gym works for body , how it different from homw workout")]}, config= configuration)
   
    if result[ '__interrupt__'] :
         llm = ChatOpenAI(model="gpt-4o-mini")
                
         result_1 = llm.invoke({"messages":HumanMessage(f"context:{result[ '__interrupt__'][-1].value} \nExtract all allowed decision options and present them in a clear, structured format with max 3-4 lines, so the user understands what each option does and when to choose it.")})
         print(result_1["messages"][-1].content)

         user_input = input("\n User : " )

         res = agent.invoke(Command(resume={"decisions":[{"type":user_input}]}),config=configuration)
         print(res["messages"][-1].content)
 
   



if __name__ == "__main__":
    agent_HumanInTheLoopMiddlewar()