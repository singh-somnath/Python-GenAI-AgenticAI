from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from uuid import uuid4
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnablePassthrough


load_dotenv()
apiKEY = os.getenv("OPENAI_API_KEY")
basellm = ChatOpenAI(model="gpt-4o-mini",api_key=apiKEY)

store = {}
prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a RAG assistant.
                    Answer the question ONLY using the provided context.
                    If the answer is not present in the context, say:
                    "I don't have enough information in the provided context.
                    Do not use outside knowledge.

                    Use the following memory to guide your responses:
                    {memory}"""),
                ("human", """Chat History:
                    {history}

                    Context:
                    {context}

                    Question: {query}

                    Provide a helpful answer based on the context above.""")
])

def getSessionStore(session_id:str) -> InMemoryChatMessageHistory:
        if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()

        return store[session_id]

def getMessageAndHistory(currentSessionStore):
    try:      

        if len(currentSessionStore.messages) > 5 :            
            oldMessages = currentSessionStore.messages[:5]         
            summary = oldMessages
            currentSessionStore.messages = currentSessionStore.messages[5:]
        else:
            summary = ""

        return {"summary" : summary , "messages" : currentSessionStore.messages}
    
    except Exception as e:
         print(e)
         raise e
      

def askLLM(userQuery:str, session_id : str):
    try:
        currentSessionStore = getSessionStore(session_id)
        message_history = getMessageAndHistory(currentSessionStore)
        currentContext = getReteriever().invoke(userQuery)
        
        ragChain = (
                {
                    "memory": lambda _: message_history["messages"],
                    "history": lambda _: message_history["summary"],
                    "context": lambda _: "",
                    "query": RunnablePassthrough()
                }
                | prompt
                | basellm
                | StrOutputParser()
        )


        content  = ragChain.invoke(userQuery,config={"configurable":{"session_id" : session_id}})

        currentSessionStore.add_user_message(userQuery)
        currentSessionStore.add_ai_message(content)

        return content
    except Exception as e:
          print(e)
          raise e        