from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from glob import glob

def getDocumentsChunks():
    docs =[]

    for path in glob("./data/*"):
        if path.lower().endswith(".txt"):
            loader = TextLoader(path)
        elif path.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            continue

        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
         chunk_size=500,
         chunk_overlap=200
    )

    chunks =splitter.split_documents(docs)   

    return chunks

