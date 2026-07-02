import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

def get_weather(city:str)->str:
    """Get the weather for a city"""
    return f"The weather in {city} is sunny"

#pydantic - runtime type system for Python applications.
class Country(BaseModel):
    capital:str
    country_code:int
    area:float
    population:int
    president:str
    continent:str
    border_countries : list[str]


def main():  
    load_dotenv()
    os.getenv("OPENAI_API_KEY")
    
    
    ###########################################################################################################################
    #Agent with Tool
    agent = create_agent(
        model="gpt-4o-mini",
        tools=[get_weather],
        system_prompt="You are a helpful assitant",
        response_format=Country
        )


    response = agent.invoke({"messages":[{"role":"user","content":"Give details about China"}]})
  
    print(response["messages"][1].content)
    print(response["structured_response"])
    print(response["messages"][1].response_metadata["token_usage"])

    ###########################################################################################################################
    #Structured Output
    model = ChatOpenAI(model="gpt-4o-mini")
    model_with_structure = model.with_structured_output(Country)
    print(model.profile)
    response = model_with_structure.invoke("Give details about England")
    print(response,sep="\n")
    

if __name__ == "__main__":
    main()