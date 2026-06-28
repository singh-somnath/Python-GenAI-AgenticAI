from mcp.server.fastmcp import FastMCP
from src.TaskManager import TaskManager

mcp = FastMCP("TaskMAnager")

@mcp.tool()
def createTaskItem(title,description):
    """This function will help to add a new task item with below arguments
       Args
       title : Task Item Title
       Description : Task Item Dscription
    """
    try:
        taskMgr = TaskManager()
        taskMgr.addTask(title,description)
    except Exception as e:
        raise e

@mcp.tool()
def editTaskItem(itemPosition,title,description):
    """This function will help to edit a existing task item with below arguments
       Args
       itemPosition : item index - it will start from 1
       title : Updated Task Item Title
       Description : Updated Task Item Dscription
    """
    try:
        taskMgr = TaskManager()
        taskMgr.editTask(itemPosition,title,description)
    except Exception as e:
        raise e

@mcp.tool()
def deleteTaskItem(index):
    """This function will help to remove an existing task item with below arguments
       Args
       index : item index - it will start from 1       
    """
    try:
        taskMgr = TaskManager()
        taskMgr.deleteTask(index)
    except Exception as e:
        raise e
    

@mcp.tool()
def showAllTask():
    """This function will help to reterieve all existing task items
       Args - No Argument           
    """
    try:
        taskMgr = TaskManager()
        return taskMgr.listTask()
    except Exception as e:
        raise e

@mcp.resource("file://taskfile/{name}")
def getTaskItem(name):
    """This function will help to reterieve a specific task file item with below arguments
       Args
       name : Task Item Title       
    """
    try:       
        return f"Task File : {name}"
    except Exception as e:
        raise e 
    

if __name__ == "__main__":
     mcp.run(transport='stdio')



"""
mcp.json content:
{
  "servers": {
    "task-manager": {
      "type": "stdio",
      "command": "F:\\Python-GenAI-AgenticAI\\ModelContextProtocol-MCP\\.venv\\Scripts\\python.exe",
      "args": [
        "server.py"
      ],
      "cwd": "F:\\Python-GenAI-AgenticAI\\ModelContextProtocol-MCP"
    }
  }
}
"""