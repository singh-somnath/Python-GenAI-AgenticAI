import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableMap,RunnableLambda

import tiktoken

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

reviewSummaryChain = PromptTemplate(
    input_variables=["review"],
    template="Please provide a 1 line summary for the review {review}"
) | base_llm | parser

sensitivityChain = PromptTemplate(
    input_variables=["review"],
    template="Please provide a sensitivity of the review either positive or negative in single word.\n Review : {review}"
) | base_llm | parser

singleReview = RunnableMap(
    summary = reviewSummaryChain,
    sensitivity = sensitivityChain
)

reviewsProcessor = RunnableLambda(
    lambda input : [ singleReview.invoke({"review":r}) for r in input["review"]]
)

def listOfReviews():

    sample_reviews=[
        "Excellent product, really enjoyed using it.",
        "Good quality and arrived on time.",
        "The product works as expected.",
        "Very satisfied with the purchase.",
        "Decent product for the price.",
        "Great experience, would recommend it.",
        "The quality could be improved.",
        "Fast delivery and good packaging.",
        "Not bad, but there is room for improvement.",
        "Overall, a good product and worth the money."
    ]

    responses = reviewsProcessor.invoke({"review" : sample_reviews})

    for i,r in enumerate(responses):
        print(f"Review : {sample_reviews[i]}")
        print(f"summary : {r['summary']}")
        print(f"summary : {r['sensitivity']}")
        print("----------------------------------------------------")

