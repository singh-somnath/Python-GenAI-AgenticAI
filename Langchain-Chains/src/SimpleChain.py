import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

def simpleChain():
    customer_feedback=f"""I have been using the iPhone 15 for a few weeks, and the overall experience has been good. The camera quality is excellent, producing sharp and vibrant photos in most lighting conditions. The performance is very smooth, and apps open quickly without any lag. However, the battery life could be better when using the phone heavily throughout the day. I also feel that the charging speed is slower compared to some competing smartphones. While the phone is reliable and well-built, the upgrades over the previous model do not always feel significant enough to justify the price.
    """

    prompt_template = PromptTemplate(
        input_variables=["feedback"],
        template="""
        Summaraize this feedback in negative and positive structure\n
        feedback : {feedback}
        """
    )

    chain = prompt_template | base_llm

    response = chain.invoke({"feedback":customer_feedback})
    
    return response.content.strip()

