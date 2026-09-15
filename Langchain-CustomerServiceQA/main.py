from src.LoadLLMandConfig import getLLMandConfig
from src.Classification import applyBatchClassification
from src.EvaluationCriteria import getEvaluationCriteria
from src.Evaluation import runEvaluation
from src.QAReport import finalReport
from src.GetExcel import genrateExcel


if __name__ == "__main__":
    #Load LLM and Data ---------------------------------------------------------------------
    settings = getLLMandConfig()
    #CLASSIFICATION-----------------------------------------------------------------------------
    df = applyBatchClassification(settings)
    #EvaluationCriteria
    df = getEvaluationCriteria(df)
    #Evaluation
    df = runEvaluation(df,settings)
    #QAReport
    df = finalReport(df,settings)
    #Generate Excel --------------------------------------------------------------------------------
    ex = genrateExcel(df)
    print("Report Generated Successfully")
