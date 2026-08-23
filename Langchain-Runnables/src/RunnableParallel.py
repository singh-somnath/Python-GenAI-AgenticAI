import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableParallel

import tiktoken

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

titleChain = PromptTemplate(
    input_variables=["interest"],
    template="Please provide a professional title for the interest {interest}"
) | base_llm | parser

summaryChain = PromptTemplate(
    input_variables=["interest"],
    template="Please provide a 5line summary for the interest {interest}"
) | base_llm | parser

def titleSummary():
    titleSummary = RunnableParallel(
        title = titleChain,
        summary = summaryChain
    )

    response = titleSummary.invoke({"interest": "AI in SharePoint for New Oppertunity"})

    print(response["title"])
    print(response["summary"])