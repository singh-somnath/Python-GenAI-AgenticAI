import pandas as pd
from dotenv import load_dotenv

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm

class TranscriptClassification(BaseModel):
    call_type:str = Field(description="Please provide type of the transcript.")
    confidence:str = Field(description="Please give Confidence score beween 0 to 1")

def getClassificationChain(settings):
    llm = settings["llm"]
    config = settings["config"]

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
    return classificationChain

def applyBatchClassification(df,settings):
    #Batch Classification
    classificationChain = getClassificationChain(settings)
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

    return df
