import json
from datetime import datetime
class Task:
    id:int
    title:str
    descrition:str
    due_date:str
    priority:str
    status:str

    def __init__(self,title,description,due_date,priority,status):
        taskMan = TaskManager()
        self.id=taskMan.getNextId()
        self.title = title
        self.descrition = description
        self.due_date = due_date
        self.priority = priority
        self.status = status

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
                self.taskList.append(Task(task["title"],task["description"],datetime.strptime(task["dueDate"],"%Y-%m-%d"),task["priority"],task["status"]))
    
    def exit(self):
        try:
            with open("./TaskManager.json","w") as file:
                data = []
                for task in self.taskList:
                    data.append({"title":task.title,"description":task.descrition,"dueDate":str(datetime.strftime(task.due_date,"%Y-%m-%d")),"priority":task.priority,"status":task.status})
                json.dump(data,file,indent=4,default=str)
        except Exception as e:
            print("File not found - Not able to write - ", e)
          
    def addTask(self):
        print("------------------------------------------------------------------------")
        print("Please provide below details to create a task : ")
        
        title = input("Task Title : ")
        description = input("Task Description : ")

        while True:
            try:
                dueDate = input("Task Due Date [YYYY-MM-DD] : ")
                parseDueDate = datetime.strptime(dueDate,"%Y-%m-%d")
            except Exception as e:
                print("Please enter valid date")
            else:
                break
        
        while True:
            try:
                priority = input("Pleas enter valid priority ['Low','Medium','High'] : ")
            except:
                print("Invalid Status")
            else:    
                if priority.lower() in ['low','medium','high']:
                    break

        while True:
            try:
                stts = input("Pleas enter valid status ['Pending','Completed','Overdue'] : ")
            except:
                print("Invalid status.")
            else:
                if stts.lower() in ['pending','completed','overdue']:
                    break
        newTask= Task(title,description,parseDueDate,priority,stts)
        self.taskList.append(newTask)
        print("------------------------------------------------------------------------")

    def deleteTask(self,index):
        try:
            index=int(index)
        except:
            print("Invalid input")
        else:
            if(index < 1 and index > len(self.taskList)):
                print("Please prodie valid index to delete the task.")
            else:
                del self.taskList[index-1]
    
    def editTask(self):
        index = ("Please rnter valid index to edit the item : ")
        if(index < 0 and index > len(self.taskList)):
            print("Index is not valid")
        else:
            print("Selected Item")
            print(f"Title : {self.taskList[index].Title}")
            print(f"Descrition : {self.taskList[index].descrition}")
            print(f"Due date : {self.taskList[index].due_date}")
            print(f"Priority : {self.taskList[index].priority}")
            print(f"Status : {self.taskList[index].status}")
            print("-------------------------------------------------------------------")
            newTitle = input("Please enter new title : ")
            newDescription = input("Please enter new description : ")
           
            while True:
                try:
                    newDueDate = input("Please enter new due date : ")
                    if not newDueDate:
                        break

                    parseDueDate = datetime.strptime(newDueDate,"%Y-%m-%d")
                except Exception as e:
                    print("Please enter valid date")
                else:
                    break
        
            while True:
                newPriority = input("Pleas enter valid new priority ['Low','Medium','High'] : ")
                if newPriority.lower() in ['low','medium','high'] and not newPriority:
                    break

            while True:
                newStts = input("Pleas enter valid new status ['Pending','Completed','Overdue'] : ")
                if newStts.lower() in ['pending','completed','overdue'] and not newStts:
                    break

            self.taskList[index].Title = newTitle if newTitle else self.taskList[index].Title
            self.taskList[index].descrition = newDescription if newDescription else self.taskList[index].descrition
            self.taskList[index].due_date = parseDueDate if newTitle else self.taskList[index].due_date
            self.taskList[index].priority = newTitle if newPriority else self.taskList[index].priority
            self.taskList[index].status = newTitle if newStts else self.taskList[index].status
            print("-------------------------------------------------------------------------------------")
            print("Edited Item")
            print(f"Title : {self.taskList[index].Title}")
            print(f"Descrition : {self.taskList[index].descrition}")
            print(f"Due date : {self.taskList[index].due_date}")
            print(f"Priority : {self.taskList[index].priority}")
            print(f"Status : {self.taskList[index].status}")
            print("-------------------------------------------------------------------------------------")
    
    def listTask(self):
        prTasks = {}
        if len(self.taskList) <= 0:
            print("Task List is empty")
            return
        
        for task in self.taskList:
            if task.priority not in prTasks:
                prTasks[task.priority] = {"tasks":[]}
            
            prTasks[task.priority]["tasks"].append(f"Title : {task.title} | Due Date : {task.due_date}")
        
        for item in prTasks:
            print(f"Priority : {item}")
            for tlistitem in prTasks[item]["tasks"]:
                print(tlistitem)
    
    def searchTask(self):
        searchText = input("Please enter tile or date ['YYYY-MM-DD'] to search task")
        try:
            parsedDate = datetime.strptime(searchText,"%Y-m-%d") or datetime.strptime(searchText,"%Y-%m")
            isDate=True
        except:
            isDate=False
        currentItem = -1
        if not isDate:
            for task in self.taskList:
                if task.title.lower() == searchText.lower():
                    currentItem = task.id
                    break
        else:
            for task in self.taskList:
                if task.due_date.year == parsedDate.year and task.due_date.year == parsedDate.year:
                    if not parsedDate.day:
                        currentItem = task.id
                        break    
                    else:
                        if task.due_dat.day == parsedDate.day:
                            currentItem = task.id
                            break  
                
        if not currentItem == -1:
                print("Task Details : ")
                print(f"Title : {self.taskList[currentItem-1].Title}")
                print(f"Descrition : {self.taskList[currentItem-1].descrition}")
                print(f"Due date : {self.taskList[currentItem-1].due_date}")
                print(f"Priority : {self.taskList[currentItem-1].priority}")
                print(f"Status : {self.taskList[currentItem-1].status}")
                print("-------------------------------------------------------------------")
        
    def showDueTaskToday(self):
        isavailable = False
        for task in self.taskList:
            if task.due_date.date() == datetime.now().date:
                print(f"Title : {task.title} | Due Date : {task.due_date}")
                isavailable = True
        
        if not isavailable:
            print("No task due for today.")

    def showPastDueTask(self):
        isavailable = False
        for task in self.taskList:
            
            if  task.due_date.date() < datetime.now().date():                
                print(f"Title : {task.title} | Due Date : {task.due_date}")
                isavailable = True
        
        if not isavailable:
            print("No past due task..")


print("Task Manager Satrted...")
taskManager = TaskManager()
while True:
    
    print("##################################################################################################################")
    print("##################################################################################################################")
    print("Please selct one of the below option :")
    print("______________________________________")
    print("1. Add Task | 2. Remove Task | 3. Edit Task | 4. Search Task | 5. List Taks | 6. Due Task Today | 7. Past Due Tak  | E Exit")

    selectedOption = input("Please enter your option : ")
   

    if selectedOption == "1":
         print("Add Task")
         taskManager.addTask()    
    elif selectedOption == "2":
        print("Remove Task")
        input = input("Please provide index of task item : ")
        taskManager.deleteTask(input)
    elif selectedOption == "3":
        print("Edit Task")
        taskManager.editTask()
    elif selectedOption == "4":
        print("Search Task")
        taskManager.searchTask()
    elif selectedOption == "5":
        print("List Tasks")
        taskManager.listTask()
    elif selectedOption == "6":
        print("Due Task Today")
        taskManager.showDueTaskToday()
    elif selectedOption == "7":
        print("Past Due Task")
        taskManager.showPastDueTask()
    elif selectedOption.lower() == "e":
        print("Exit")
        taskManager.exit()
        break      
    else:
        print("Please choose valid option")   

print("Task Manager Stopped...")