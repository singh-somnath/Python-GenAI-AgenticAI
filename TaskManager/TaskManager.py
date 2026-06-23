from datetime import datetime

class Task:
    def __init__(self,title,description,dueDate,priority,status="Created"):
        self.title = title
        self.description = description
        self.dueDate = dueDate
        self.priority = priority
        self.status = status

class TaskManager:
    def __init__(self):
        self.tasks = []

    def addNewTask(self,task):
        self.tasks.append(task)

    def removeTaskByTitle(self,title):
        for task in self.tasks:
            if task.title.lower() == title.lower() :
                self.tasks.remove(task)
    
    def listAllTasks(self):
        for task in self.tasks:
            print("-------------------------------------------------------")
            print("Task Details")
            print(f"Title : {task.title}")
            print(f"Description : {task.description}")
            print(f"Due Date : {datetime.strftime(task.dueDate,'%m-%d-%Y')}")
            print(f"Priority : {task.priority}")
            print(f"Status : {task.status}")


        

taskManager = TaskManager() 

while True:
    print("#########################################################")
    print("Please select any one option")
    print("1 - Add a new task")
    print("2 - Remove an existing task")
    print("3 - List all high priority Taks")
    print("4 - Group tasks by priority")
    print("5 - Exit")
    selectedOption = int(input("Enter your option : "))

    if selectedOption == 5:
        break
    elif selectedOption == 1:
        taskTitle = input("Enter a task title:")
        taskDescription = input("Enter task description:")
        while True:
            try:
                taskDueDate = datetime.strptime(input("Enter task due date:"),"%m-%d-%Y")
            except:
                print("Please provide valid date")
            else:
                break
        while True:
            taskPriority = input("Enter task priority[High/Medium/Low]:")
            if taskPriority.lower() == "high" or taskPriority.lower() == "medium" or taskPriority.lower() == "low":
                taskPriority = taskPriority.upper()
                break
            else:
                print("Please enter valid value [High/Medium/Low].")

        newTask = Task(taskTitle,taskDescription,taskDueDate,taskPriority)
        taskManager.addNewTask(newTask)
    elif selectedOption == 3:
        taskManager.listAllTasks()


