import pandas as pd
from tqdm import tqdm

#EVALUATION CRITERIA -------------------------------------------------------------------------------
def getEvaluationCriteria(df):
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