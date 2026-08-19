import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

with open("config.json","r") as f:
    config= json.load(f)

provider = config["provider"]

def get_llm():
    if provider == "openai":
        return ChatOpenAI(
            model=config[provider]["model"],
            temperature=config[provider]["temprature"],
            max_completion_tokens= config[provider]["max_token"],
            api_key=os.getenv("OPENAI_API_KEY")            
        )
    elif provider == "groq":
         return ChatGroq(
                    model=config[provider]["model"],
                    temperature=config[provider]["temprature"],
                    max_tokens=config[provider]["max_token"],
                    api_key=os.getenv("GROQ_API_KEY")            
        )
    elif provider == "gemini":
         return ChatGoogleGenerativeAI(
                            model=config[provider]["model"],
                            temperature=config[provider]["temprature"],                           
                            api_key=os.getenv("GEMINI_API_KEY"),
                            max_tokens=config[provider]["max_token"],       
         )
    else:
        raise ValueError("Not valid provider.")

   