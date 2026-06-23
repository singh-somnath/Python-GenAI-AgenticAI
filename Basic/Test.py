class Employee:
    
    def __init__(self,name,id,floor,deskNo):
        self.name = name
        self.id=id
        self.floor=floor
        self.deskNo=deskNo

    
class EmployeeManager:
    def __init__(self):
        self.employees=[]
    
    def addEmployee(self, emp):
        self.employees.append(emp)

    def removeEmployee(self,index):
        del self.employees[index-1]

    def showEmployee(self):
        print("####################################################")
        print("List of Employee")
        for emp in self.employees:
            print("-------------------------------------------------------")
            print("Name : " + emp.name)
            print("Id : " + emp.id)
            print("Floor : " + emp.floor)
            print("Desk No : " + emp.deskNo)
    
    def showEmployeeFloorWise(self):
        floorWiseList={}
        for emp in self.employees:
            if emp.floor not in floorWiseList:
                floorWiseList[emp.floor]={"List":[]}

            floorWiseList[emp.floor]["List"].append(f"Name : {emp.name} | ID : {emp.id} | Desk No : {emp.deskNo} ")


        for floor in floorWiseList:
            print(f"Floor : {floor}")
            for emp in floorWiseList[floor]["List"]:
                print(f"{emp}")


empMng =  EmployeeManager()

emp = Employee("Somnath 1","123","Floor 1","2036")
empMng.addEmployee(emp)
emp = Employee("Somnath 2","131","Floor 2","2031")
empMng.addEmployee(emp)
emp = Employee("Somnath 3","131","Floor 4","2031")
empMng.addEmployee(emp)
emp = Employee("Somnath 4","131","Floor 4","2031")
empMng.addEmployee(emp)
emp = Employee("Somnath 4","131","Floor 2","2031")
empMng.addEmployee(emp)
emp = Employee("Somnath 4","131","Floor 3","2031")
empMng.addEmployee(emp)
emp = Employee("Somnath 4","131","Floor 3","2031")
empMng.addEmployee(emp)
empMng.showEmployeeFloorWise()
#empMng.showEmployee()
#empMng.removeEmployee(3)
#empMng.showEmployee()