from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import TextLoader


def load_all_documents(data_dir:str) -> List[Any]:
    """
    Load all supported files
    """
    documents=[]
    #Load PDF files add in documents
    for pdf in list(Path(data_dir).glob("./pdf_files/*.pdf")):
        pdfFile = PyMuPDFLoader(pdf)
        pdfLoad = pdfFile.load()
        
        for doc in pdfLoad:
            doc.metadata["file_name"] = pdf.name
            doc.metadata["file_type"] = "pdf"

        documents.extend(pdfLoad)
       

    #Load EXCEL files add in documents
    for excel in list(Path(data_dir).glob("./excel_files/*.xlsx")):
        excelFile = UnstructuredExcelLoader(excel)
        excelLoad = excelFile.load()
        
        for doc in excelLoad:
            doc.metadata["file_name"] = excel.name
            doc.metadata["file_type"] = "excel"

        documents.extend(excelLoad)

    #Load Word files add in documents
    for word in list(Path(data_dir).glob("./word_files/*.docx")):
        wordFile = UnstructuredWordDocumentLoader(word)
        wordLoad = wordFile.load()
        
        for doc in wordLoad:
            doc.metadata["file_name"] = word.name
            doc.metadata["file_type"] = "word"

        documents.extend(wordLoad)
    

    #Load TXT files add in documents
    for txt in list(Path(data_dir).glob("./text_files/*.txt")):
        txtFile = TextLoader(txt)
        txtLoad = txtFile.load()
        
        for doc in txtLoad:
            doc.metadata["file_name"] = txt.name
            doc.metadata["file_type"] = "text"

        documents.extend(txtLoad)

  
    return documents


