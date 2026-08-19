import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

messages = [
    "My laptop has been experiencing frequent system crashes for the past week, and despite raising a ticket, the issue has not been resolved. This is affecting my daily work and productivity.",
    "I am unable to access the company VPN since yesterday. Multiple attempts to contact support have resulted in no update, and I urgently need access to complete my tasks.",
    "The product specifications provided by the sales team were inaccurate, and the delivered item does not meet the requirements discussed during the purchase process.",
    "I am disappointed with the delayed response from the sales team regarding my pricing and renewal inquiries. The lack of communication has made the purchasing process difficult.",
    "I reported an issue with my payroll details two weeks ago, but I have not received any update or resolution. I would appreciate a prompt response, as this is causing significant inconvenience."
]

sales_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
            You are an sales representative and provide an valid answer for below complaint.\n
            complaint : {message}
    """
)
saleschain = sales_prompt | base_llm | parser

tech_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
            You are an technical support representative and provide an valid answer for below complaint.\n
            complaint : {message}
    """
)
techchain = tech_prompt | base_llm | parser

hr_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
            You are an HR support representative and provide an valid answer for below complaint.\n
            complaint : {message}
    """
)
hrchain = hr_prompt | base_llm | parser

router_prompt = PromptTemplate(
    input_variables=["message"],
    template="""
            Please analyze the below complaint message and give the type of it either of these three - HR, Sales or Technical. Please donot change the type or use any other word for the type\n
            complaint : {message}
    """
)
routerchain = router_prompt | base_llm | parser


router = RunnableBranch(
    (
        lambda x : "sales" in x.lower(),
        saleschain,
    ), 
    (
        lambda x : "technical" in x.lower(),
        techchain,
    ), 
    (
        lambda x : "hr" in x.lower(),
        hrchain,
    ),
    RunnablePassthrough
)

def routerChainExample():
    print("Message")
    print(messages[1])
    category = routerchain.invoke({"message" : messages[1]})
    print(f"Category : {category}" )
    response = router.invoke(category)
    print(response)