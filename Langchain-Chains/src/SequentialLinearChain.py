import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)
parser = StrOutputParser()

summaryTemplate = PromptTemplate(
    input_variables=["feedback"],
    template="""
            Please provide the summary of this customer feeback \n
            feddback : {feedback}
    """
)

summaryChain = summaryTemplate | base_llm | parser

sentimentTemplate = PromptTemplate(
    input_variables=["summary"],
    template="""
            Please provide the sentiment of this summary in one positive , negative or neutral \n
            summary : {summary}
    """
)

sentimentChain = sentimentTemplate | base_llm | parser

reexpressTemplate = PromptTemplate(
    input_variables=["summary","sentiment"],
    template="""
            Please re express this  summary with the provided sentiment  in 4 points with some header \n
            summary : {summary} \n
            sentiment : {sentiment}
    """
)

reexpressChain = reexpressTemplate | base_llm | parser

def reexpress():
    customer_feedback=f"""
                       Bangalore traffic has become increasingly frustrating, with daily commutes often taking much longer than expected. Even short distances can sometimes require an hour or more during peak hours. Frequent congestion at major junctions leads to delays and added stress for commuters. Road construction, narrow roads, and the growing number of vehicles contribute significantly to the problem. Public transportation improvements have not always kept pace with the city's rapid expansion. Overall, the traffic situation negatively impacts productivity, work-life balance, and the overall quality of life for many residents.
                       """
    summary = summaryChain.invoke({"feedback":customer_feedback})
    sentiment = sentimentChain.invoke({"summary" : summary})
    reexpress = reexpressChain.invoke({"summary":summary,"sentiment":sentiment})

    return reexpress
