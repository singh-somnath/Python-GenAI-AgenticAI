from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.retriever import basicRetriever
from src.ebmedding import getEmbedding
from src.vectorStore import getVectorDB
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=apikey,
        temperature=0.2
) 

class APPOutputStructure(BaseModel):
    question:str = Field(description="IT is representing the question or query that system asked")
    answer:str = Field(description="representing the answer")

parser = PydanticOutputParser(pydantic_object=APPOutputStructure)
format_instructions = parser.get_format_instructions()

def rag_chain():
    prompt = ChatPromptTemplate.from_messages([
         ("system", """You are a helpful assistant. Answer the user's question based ONLY on the provided context.
           Rules:
            - If the context does not contain enough information, say "I don't have enough information to answer this question."
            - Do not make up or hallucinate information.
            - Keep answers concise and relevant.
            - Explain relevant answers in minimum 3 lines
           Context: {context}
           format Instructions: {format_instructions}"""),
         ("user", "{question}")
    ])

    embedding_model = getEmbedding("Local")
    db = getVectorDB(embedding_model,type="FAISS")
    retriever = basicRetriever(db)

    rag_chain = RunnableParallel({
        "context":RunnableLambda(lambda x : x["question"]) | retriever,
        "format_instructions" : RunnableLambda(lambda _ : format_instructions),
        "question":RunnableLambda(lambda x : x["question"])
    }) | prompt | llm | parser

    return rag_chain
      

