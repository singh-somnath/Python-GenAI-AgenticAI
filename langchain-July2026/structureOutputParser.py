import os
import json
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field

load_dotenv()
openapikey = os.getenv("OPENAI_API_KEY")
base_llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openapikey
)

#Structure Schema With TypedDict
class ProductInfo(TypedDict):
    product_name:str
    category:str
    key_features: list[str]    

def structureSchemaTypedDict():
    llm = base_llm.with_structured_output(ProductInfo)
    #prepare prompt and run query
    prompt = "Extract the product name, category, and 3 key features "
    "from the following description:\n\n"
    "The new SoundMax Pro X headphones deliver superior bass, "
    "active noise cancellation, and 30 hours of wireless playback. "
    "They are perfect for travel and studio use."

    print("Structure Output - TypeDict")
    print(llm.invoke(prompt))

#Structure Schema With PYDANTIC
class BookInfo(BaseModel):
    title:str = Field(...,description="This is the title of the book")
    author : str = Field(...,description="This is author of the book")
    genre : str = Field(...,description="This is the genre of the book")
    key_themes : list[str] = Field(...,description="This provide key themes of the book")

def structureOutPutPydentic():
    llm = base_llm.with_structured_output(BookInfo)
    print(llm.invoke("Please provide details of the Harryporter first part book"))

#JSON Schema
def structureOutputJsonSchema():
    with open("BookSchema.json") as file:
       rowSchema =  json.load(file)

    llm = base_llm.with_structured_output(rowSchema)

    print(llm.invoke("Give me details about the Let us c book"))
    
def main():
    structureOutputJsonSchema()
    



if __name__ == "__main__":
    main()