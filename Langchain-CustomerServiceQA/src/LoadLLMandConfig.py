import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#Load LLM and Data ---------------------------------------------------------------------
load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

def getLLMandConfig():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=apikey,
        temperature=0.3
    )

    with open("config/config.json","r") as f:
        config = json.load(f)

    return {"llm":llm,"config":config}