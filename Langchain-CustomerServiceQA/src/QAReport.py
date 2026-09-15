

import pandas as pd

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm




#Final Report
class QAManagerResponse(BaseModel):
    summary:str = Field(description="Overall evaluation summary")
    recommendations:list[str] = Field(description="List of recommendations")

def getQAReportChain(llm):
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
    return qaReportChain

def finalReport(df:pd.DataFrame,settings):
    resultFinal=[]
    llm=settings["llm"]
    for i, row in tqdm(df.iterrows(),total=len(df),desc="Generating Final Report"):
        try:
            result = getQAReportChain(llm).invoke({"evaluation_output" : row["evaluation_output"]})
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