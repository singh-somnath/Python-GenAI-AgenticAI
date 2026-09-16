import os
from fastapi import FastAPI,UploadFile,HTTPException,status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import pandas as pd
from main import getCustomerSupportQAReport

os.makedirs("data",exist_ok=True)

app = FastAPI(
    title="Customer Support QA Evaluator",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def health():
    return {"status":"ok"}


@app.post("/evaluate-file")
async def evaluateFile(file:UploadFile):
    allowedExtension = [".csv",".xlsx"]
    f_extension = os.path.splitext(file.filename)[1].lower()

    if f_extension not in allowedExtension:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="File not allowed") 

    inputPath = f"data/inputData_{uuid.uuid4()}{f_extension}"
    outputPath = f"data/output_{uuid.uuid4()}.xlsx"

    with open(inputPath,"wb") as f:
        content = await file.read()
        f.write(content)

    if f_extension == ".csv":
        df = pd.read_csv(inputPath)

    if f_extension == ".xlsx":
        df = pd.read_excel(inputPath)

    getCustomerSupportQAReport(df,outputPath)

    return FileResponse(
        path=outputPath,
        status_code=status.HTTP_201_CREATED,
        filename="output.xlsx"
    )
