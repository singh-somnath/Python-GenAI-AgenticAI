from mcp_use import MCPClient, MCPAgent
import os
import asyncio
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

async def run_memory_chat():
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
    client = MCPClient.from_config_file("./config.json")
    agent = MCPAgent(
        llm=llm,
        client=client,
        memory_enabled=True
    )
   
    try:
        print("----Initializing Chat")
        print("--Enter 'exit' for exit")
        while True:
            user_input = input("\n User : ")
            
            if user_input.lower() in ["exit","quit"]:
                break

            print("\n Assistant : ")
            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"Error : {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())



