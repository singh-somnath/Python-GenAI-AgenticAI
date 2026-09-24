from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from glob import glob

def getDocumentsChunks() -> list[Document]:
    docs =[]
    docID =1

    for path in glob("./data/*"):
        if path.lower().endswith(".txt"):
            loader = TextLoader(path)
        elif path.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            continue

        currentDocs = loader.load()
        for doc in currentDocs:
            doc.metadata["docID"] = docID
            docID = docID + 1

        docs.extend(currentDocs)

    splitter = RecursiveCharacterTextSplitter(
         chunk_size=500,
         chunk_overlap=200
    )

    chunks =splitter.split_documents(docs)   

    for i,chunk in enumerate(chunks,start=1):
            chunk.metadata["chunkID"] =   str(chunk.metadata["docID"]) + "_" + str(i)            

    return chunks

