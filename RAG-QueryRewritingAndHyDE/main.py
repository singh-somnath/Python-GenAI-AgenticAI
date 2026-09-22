from dotenv import load_dotenv
load_dotenv()

from src.loader import getDocumentsChunks
from src.reteriever import getReteriever, getQueryEmbedding
from langchain_core.chat_history import InMemoryChatMessageHistory
from src.llmResponse import askLLM

def main():
    try:
        #chunks = getDocumentsChunks()
        #vectorStore = getReteriever(chunks)
        #docs = vectorStore.invoke(query)
        #for doc in docs:
        #    print(doc)
        while True:
            inputQ =input("Enter your query [For stop enter exit] : ")

            if inputQ.lower() == "exit":
                break

            print("Response : ")
            print(askLLM(inputQ,"user-123"))

        print("------------End--------------")

    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    main()
