from dotenv import load_dotenv
load_dotenv()

from src.multiLevelReteriver import multiLevelReteriever
#from src.llmResponse import askLLM

def main():
    try:
        #chunks = getDocumentsChunks()
        #vectorStore = getReteriever(chunks)
        #docs = vectorStore.invoke(query)
        #for doc in docs:
        #    print(doc)
        while True:
            print("--------------------------")
            inputQ =input("Enter your query [For stop enter exit] : ")

            if inputQ.lower() == "exit":
                break

            #print("Response : ")
            #print(askLLM(inputQ,"user-123"))
            multiLevelReteriever(inputQ)

        print("------------End--------------")

    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    main()
