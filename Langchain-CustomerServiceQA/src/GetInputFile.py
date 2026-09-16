import pandas as pd

def getInputFileDF(path:str):   
    df = pd.read_csv(path)
    return df

