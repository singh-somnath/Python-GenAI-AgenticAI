import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, BSHTMLLoader, UnstructuredURLLoader
import requests
import tempfile


def textDocLoader():
    if os.path.exists("sample-data/sample.txt"):
         textLoader = TextLoader(file_path="sample-data/sample.txt")
         textDoc = textLoader.load()
         print(f"Pages of file {len(textDoc)}")
         return textDoc
    else:
         print(f"Text file does not exist")

def pdfDocLoader():
     filePath = "sample-data/NIPS-2017-attention-is-all-you-need-Paper.pdf"
     if os.path.exists(filePath):
        pdfLoader = PyPDFLoader(file_path=filePath)
        pdfDoc = pdfLoader.load()
        print(f"Pages of file {len(pdfDoc)}")
        return pdfDoc
     else:
        print(f"Text file does not exist")

def bsHtmlFileLoader(): #Static WePage
    url="https://www.wps.com"
    html = requests.get(url).text

    temppath = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
    with open(temppath,"w",encoding="utf-8") as f:
        f.write(html)
    
    htmlLoader = BSHTMLLoader(temppath, open_encoding="utf-8", bs_kwargs={'features': 'html.parser'})
    htmlDoc = htmlLoader.load()

    print(f"Page : {len(htmlDoc)}")
    return htmlDoc
     
def unsturucteredUrlLoader():
    urls={
        "https://voters.eci.gov.in/",
        "https://www.langchain.com/pricing"
    }  

    urlLoader = UnstructuredURLLoader(urls=urls)
    urlDocs = urlLoader.load()

    print(f"No of pages : {len(urlDocs)}")
    return urlDocs
   