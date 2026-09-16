from src.LoadLLMandConfig import getLLMandConfig
from src.Classification import applyBatchClassification
from src.EvaluationCriteria import getEvaluationCriteria
from src.Evaluation import runEvaluation
from src.QAReport import finalReport
from src.GetExcel import genrateExcel
from src.GetInputFile import getInputFileDF

def getCustomerSupportQAReport(df,outputpath):
     #Load LLM and Data ---------------------------------------------------------------------
    settings = getLLMandConfig()    
    #CLASSIFICATION-----------------------------------------------------------------------------
    df = applyBatchClassification(df,settings)
    #EvaluationCriteria
    df = getEvaluationCriteria(df)
    #Evaluation
    df = runEvaluation(df,settings)
    #QAReport
    df = finalReport(df,settings)
    #Generate Excel --------------------------------------------------------------------------------
    genrateExcel(df,outputpath)



if __name__ == "__main__":
    getCustomerSupportQAReport("data/transcripts.csv","data/output.xlsx")
   
