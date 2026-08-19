import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

parser = StrOutputParser()

product_description = f"""
I purchased a 16GB DDR5 RAM kit to upgrade my desktop computer, and the improvement in performance was noticeable immediately. Applications open faster, and multitasking has become much smoother than before. The RAM operates at high speed and works reliably even when running multiple programs simultaneously. Installation was straightforward, and the system recognized the memory without any issues. Gaming performance has also improved, with fewer stutters and better overall responsiveness. The build quality of the RAM modules feels solid and premium. However, the price is slightly higher compared to some competing brands with similar specifications. The RGB lighting looks attractive and adds a modern touch to the system. After several weeks of use, I have not experienced any stability problems or crashes. Overall, this RAM upgrade provides excellent performance and is a worthwhile investment for productivity and gaming users.
"""

featureTemplate = PromptTemplate(
    input_variables=["description"],
    template="""
    Give all the main fearues of the below product in markdown format\n
    Product Description : {description}
    """
)

featureChain = featureTemplate | base_llm | parser

adTemplate = PromptTemplate(
    input_variables=["description"],
    template="""
    Give a professional advertisement for the  below product in markdown format\n
    Product Description : {description}
    """
)

adChain = adTemplate | base_llm | parser

seoTemplate = PromptTemplate(
    input_variables=["description"],
    template="""
    Give me professional search engine tags or seo tags for the below product in markdown format\n
    Product Description : {description}
    """
)

seoChain = seoTemplate | base_llm | parser

multiChain = RunnableParallel(
    {
        "features" : featureChain,
        "advertisement" : adChain,
        "seotags" : seoChain
    }
)


def nonLinearChain():
    response =  multiChain.invoke({"description" : product_description})
    print("features")
    print(response["features"])
    print("Advertisement")
    print(response["advertisement"])
    print("SEO Tags")
    print(response["seotags"])
    
