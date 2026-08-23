import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

import tiktoken

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

titlePrompt = PromptTemplate(
    input_variables=["interest"],
    template="Please provide a professional title for the interest {interest}"
)

titelChain = titlePrompt | base_llm | parser

outlinePrompt = PromptTemplate(
    input_variables=["title"],
    template="Please provide an professional outline for the topic title {title}"
)

outlineChain = outlinePrompt | base_llm | parser


def chainBasedPipeline():
    title = titelChain.invoke({"interest":"Cooking, AI and Fatherhood"})
    outline = outlineChain.invoke({"title":title})
    print(outline)

