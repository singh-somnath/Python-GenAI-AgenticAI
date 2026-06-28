import json
from datetime import datetime

class Task:
    id:int
    title:str
    descrition:str
    

    def __init__(self,title,description,id=None):
        taskMan = TaskManager()
        self.id= id if id is not None else taskMan.getNextId()
        self.title = title
        self.descrition = description
    
class TaskManager:
    taskList:list[Task]
    def getNextId(self):
        return len(self.taskList) + 1
    
    def __init__(self):
        try:
            with open("./TaskManager.json","r") as file:
                data = json.load(file)
        except:
            self.taskList = []
        else:
            self.taskList = []
            for task in data:
                self.taskList.append(Task(task["title"],task["description"],task["id"]))

    def fileWrite(self):
        try:
            with open("./TaskManager.json","w") as file:
                data = []
                for task in self.taskList:
                    data.append({"id":task.id,"title":task.title,"description":task.descrition})
                json.dump(data,file,indent=4,default=str)
        except Exception as e:
            raise ValueError("File not found - Not able to write - ", e)
          
    def addTask(self,title,description):      
        newTask= Task(title,description)
        self.taskList.append(newTask)
        self.fileWrite()

    def deleteTask(self,index):
        try:
            del self.taskList[int(index)-1]
            self.fileWrite()
        except Exception as e:
           raise e    
                
    
    def editTask(self,itemPosition,newTitle,newDescription):
       try:
            index = int(itemPosition) - 1
            self.taskList[index].title = newTitle if newTitle else self.taskList[index].title
            self.taskList[index].descrition = newDescription if newDescription else self.taskList[index].descrition
            self.fileWrite()
       except Exception as e:
           raise e
          
    def listTask(self):
        prTasks = {}
        if len(self.taskList) <= 0:
           raise ValueError("No data available")
        
        for task in self.taskList:
            prTasks[task.id] = (f"Task ID : {task.id} | Title : {task.title} | Description : {task.descrition}")
        
        return prTasks
     
    
    def searchTask(self,searchTitle):       
        try:
             for task in self.taskList:
                if task.title.lower() == searchTitle.lower():
                    currentItem = task.id
                    break
            
             
                    
             return self.taskList[currentItem-1] if currentItem else None
             
        except Exception as e:
            raise ValueError("No item exist")
            
