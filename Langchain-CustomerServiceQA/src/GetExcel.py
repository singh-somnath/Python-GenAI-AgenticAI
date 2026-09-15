import pandas as pd

def genrateExcel(df : pd.DataFrame):
    return df.to_excel("data/output.xlsx",index=False)
    
