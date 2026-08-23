import os
import json
import pandas as pd
from dotenv import load_dotenv

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from tqdm import tqdm

#Load LLM and Data ---------------------------------------------------------------------
load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=apikey,
    temperature=0.3
)

df = pd.read_csv("data/transcripts.csv")

with open("config/config.json","r") as f:
    config = json.load(f)

#CLASSIFICATION-----------------------------------------------------------------------------
class TranscriptClassification(BaseModel):
    call_type:str = Field(description="Please provide type of the transcript.")
    confidence:str = Field(description="Please give Confidence score beween 0 to 1")

parserClassification = PydanticOutputParser(pydantic_object=TranscriptClassification)

promptClassification = PromptTemplate(
    input_variables=["transcript"],
    partial_variables={
        "labels":config["classification"]["labels"],
        "format_instructions" : parserClassification.get_format_instructions()
    },
    template="""
    You are an classifier assistant that help to classify transcript in only one type.
    Transcript : {transcript}
    Please use below type as option, choose any one based on the transcript from here only.
    {labels} 

    {format_instructions}
    """
)

classificationChain = promptClassification | llm | parserClassification

#Batch Classification
results=[]
for i, row in tqdm(df.iterrows(),total=len(df),desc="Classifying Calls Type"):
    try:
        response = classificationChain.invoke({"transcript":row["transcript"]})
        results.append({
            "call_id" : row["call_id"],
            "pridicted_call_type" : response.call_type,
            "confidence_Score" : response.confidence
        })
    except:
        print(f"Error at row - {i} ❌")
        results.append({
            "call_id" : row["call_id"],
            "pridicted_call_type" : "None",
            "confidence_Score" : "None"
        })

results_df = pd.DataFrame(results)
df = df.merge(results_df,on="call_id")    

#EVALUATION CRITERIA -------------------------------------------------------------------------------
def evaluationCriteria(df):
    resultsCriteria=[]
    for i,row in tqdm(df.iterrows(),total=len(df), desc="Evaluating Criteria"):
        if row["pridicted_call_type"] == "billing" or row["pridicted_call_type"] == "claims":
            resultsCriteria.append({
                "call_id" : row["call_id"],
                "evaluation_criteria" : "knowledge_accuracy,resolution_quality"
            })
        elif row["pridicted_call_type"] == "complaint" :
            resultsCriteria.append({
                "call_id" : row["call_id"],
                "evaluation_criteria" : "tone_empathy,resolution_quality"
            })
        elif row["pridicted_call_type"] == "general_query" :
            resultsCriteria.append({
                "call_id" : row["call_id"],
                "evaluation_criteria" : "knowledge_accuracy"
            })
        else:
            resultsCriteria.append({
                "call_id" : row["call_id"],
                "evaluation_criteria" : "knowledge_accuracy"
            })

    resultsCriteria_df = pd.DataFrame(resultsCriteria)
    df =  df.merge(resultsCriteria_df,on="call_id")        
    return df

#EVALUATION ----------------------------------------------------------------------------------------
class ToneEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

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

class resolutionEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

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

class knowledgeEvaluation(BaseModel):
    score:int = Field(description="Score between 1 to 5")
    reasoning:str = Field(description="Explain the score")

parserKnowledgeEvaluation = PydanticOutputParser(pydantic_object=knowledgeEvaluation)

promptKnowledge = PromptTemplate(
    input_variables=["transcript"],
    partial_variables={
        "format_instructions" : parserResolutionEvaluation.get_format_instructions()
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

def runEvaluation(df:pd.DataFrame):
    resultsEvaluation=[]
    for i,row in tqdm(df.iterrows(),total=len(df),desc="Running Evaluation"):
        result={}
        if "knowledge_accuracy" in row["evaluation_criteria"]:
            try:
                response = knowledgeChain.invoke({"transcript":row["transcript"]})
                result["knowledge"] = response.model_dump()
            except:
                result["knowledge"] = "None"

        if "resolution_quality" in row["evaluation_criteria"]:
            try:
                result["resolution"] = (resolutionChain.invoke({"transcript":row["transcript"]})).model_dump()
            except:
                result["resolution"] = "None"

        if "tone_empathy" in row["evaluation_criteria"]:
            try:
                result["tone"] = (toneChain.invoke({"transcript":row["transcript"]})).model_dump()
            except:
                result["tone"] = "None"

        resultsEvaluation.append({
            "call_id" : row["call_id"],
            "evaluation_output" : result
        })

    resultsEvaluation_df = pd.DataFrame(resultsEvaluation)
    df = df.merge(resultsEvaluation_df,on="call_id")
    return df
        
#Final Report
class QAManagerResponse(BaseModel):
    summary:str = Field(description="Overall evaluation summary")
    recommendations:list[str] = Field(description="List of recommendations")

parseQAManagerResponse = PydanticOutputParser(pydantic_object=QAManagerResponse)

promptQAReport = PromptTemplate(
    template="""
    You are a QA manager. Analyze the evaluation output and generate a summary with recommendations.
    Evaluation Output: {evaluation_output}
    Summarize key findings and provide actionable recommendations for agent improvement.
    {format_instructions}
    """,
    input_variables=["evaluation_output"],
    partial_variables={
        "format_instructions" : parseQAManagerResponse.get_format_instructions()
    }
)

qaReportChain = promptQAReport | llm | parseQAManagerResponse

def finalReport(df:pd.DataFrame):
    resultFinal=[]
    for i, row in tqdm(df.iterrows(),total=len(df),desc="Generating Final Report"):
        try:
            result = qaReportChain.invoke({"evaluation_output" : row["evaluation_output"]})
            resultFinal.append({
                "call_id":row["call_id"],
                "summary" : result.summary,
                "recommendations" : "\n".join(result.recommendations)
            })
        except:
             resultFinal.append({
                "call_id":row["call_id"],
                "summary" : "none",
                "recommendations" : "none"
            })

    resultFinal_df = pd.DataFrame(resultFinal)
    df = df.merge(resultFinal_df, on="call_id")
    return df


#Generate Excel --------------------------------------------------------------------------------
def genrateExcel(df : pd.DataFrame):
    df.to_excel("data/output.xlsx",index=False)
    print("Report Generated Sucessfully")


#Exceution -----------------------------------------------------------------------------------------
def process():
    global df
    #print(llm.invoke("Hello"))
    df = evaluationCriteria(df)
    print(df.head())   
    df = runEvaluation(df)
    print(df.head())  
    df = finalReport(df)
    print(df.head())  
    genrateExcel(df)
    
    #print(config["classification"]["labels"])
    #print(classificationChain.invoke(df.iloc[3]["transcript"]))
