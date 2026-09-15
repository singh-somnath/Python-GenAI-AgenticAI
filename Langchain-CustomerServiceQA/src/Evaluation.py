
import pandas as pd

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm




#EVALUATION ----------------------------------------------------------------------------------------
class ToneEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

def getToneChain(llm):

    parserToneEvaluation = PydanticOutputParser(pydantic_object=ToneEvaluation)

    promptTone = PromptTemplate(
        input_variables=["transcript"],
        partial_variables={
            "format_instructions" : parserToneEvaluation.get_format_instructions()
        },
        template="""
            You are a customer service tone evaluator. 
            Analyze the transcript and evaluate the agent's tone and empathy.
            Transcript: {transcript}
            Evaluate the agent on professionalism, empathy, patience, and emotional appropriateness.
            {format_instructions}
        """
    )

    toneChain = promptTone | llm | parserToneEvaluation
    return toneChain

class resolutionEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

def getResolutionChain(llm):
    parserResolutionEvaluation = PydanticOutputParser(pydantic_object=resolutionEvaluation)

    promptResolution = PromptTemplate(
        input_variables=["transcript"],
        partial_variables={
            "format_instructions" : parserResolutionEvaluation.get_format_instructions()
        },
        template="""
        You are a customer service resolution evaluator. 
        Analyze the transcript and evaluate the resolution quality.
        Transcript: {transcript}
        Assess if the issue was resolved, solution effectiveness, and whether follow-up is needed.
        {format_instructions}
        """
    )

    resolutionChain = promptResolution | llm | parserResolutionEvaluation
    return resolutionChain

class knowledgeEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

def getKnowledgeChain(llm): 

    parserKnowledgeEvaluation = PydanticOutputParser(pydantic_object=knowledgeEvaluation)

    promptKnowledge = PromptTemplate(
        input_variables=["transcript"],
        partial_variables={
            "format_instructions" : parserKnowledgeEvaluation.get_format_instructions()
        },
        template="""
        You are a customer service knowledge evaluator. 
        Analyze the transcript and evaluate the agent's knowledge accuracy.

        Transcript: {transcript}
        Assess correctness of information provided, product/policy knowledge, and error-free responses.

        {format_instructions}
        """
    )

    knowledgeChain = promptKnowledge | llm | parserKnowledgeEvaluation
    return knowledgeChain

def runEvaluation(df:pd.DataFrame,settings):
    resultsEvaluation=[]
    llm = settings["llm"]
    for i,row in tqdm(df.iterrows(),total=len(df),desc="Running Evaluation"):
        result={}
        if "knowledge_accuracy" in row["evaluation_criteria"]:
            try:
                response = getKnowledgeChain(llm).invoke({"transcript":row["transcript"]})
                result["knowledge"] = response.model_dump()
            except:
                result["knowledge"] = "None"

        if "resolution_quality" in row["evaluation_criteria"]:
            try:
                result["resolution"] = (getResolutionChain(llm).invoke({"transcript":row["transcript"]})).model_dump()
            except:
                result["resolution"] = "None"

        if "tone_empathy" in row["evaluation_criteria"]:
            try:
                result["tone"] = (getToneChain(llm).invoke({"transcript":row["transcript"]})).model_dump()
            except:
                result["tone"] = "None"

        resultsEvaluation.append({
            "call_id" : row["call_id"],
            "evaluation_output" : result
        })

    resultsEvaluation_df = pd.DataFrame(resultsEvaluation)
    df = df.merge(resultsEvaluation_df,on="call_id")
    return df