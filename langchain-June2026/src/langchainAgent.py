import os
from dotenv import load_dotenv
from langchain.agents import create_agent
#from langchain_openai import ChatOpenAI


def get_weather(city:str)->str:
    """Get the weather for a city"""
    return f"The weather in {city} is sunny"



def main():  
    load_dotenv()
    os.getenv("OPENAI_API_KEY")
    
    ##########################################################################################################################
    #Streaming
    #model = ChatOpenAI(model="gpt-4o-mini")
    #for chunk in model.stream("Why does body pain"):
        #print(chunk.text, end="")
    
    ###########################################################################################################################
    #Agent with Tool
    agent = create_agent(
        model="gpt-4o-mini",
        tools=[get_weather],
        system_prompt="You are a helpful assitant"
        )

    response = agent.invoke({"messages":"Write me 200 words paragraph on Artificial Inteligence"})
    print(response)
    print(response["messages"][1].content)    

if __name__ == "__main__":
    main()