import pandas as pd

def genrateExcel(df : pd.DataFrame,outputPath):
    df.to_excel(outputPath,index=False)
    
