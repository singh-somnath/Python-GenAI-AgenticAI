from colorama import Fore
import json
from datetime import datetime
import matplotlib.pyplot as plt
#from plyer import notification


class Expense:
    def __init__(self,date,category,amount,note):
        self.date=date
        self.category=category
        self.amount=amount
        self.note=note

class ExpenseManager:
    def __init__(self):
        self.expenses = []
    
    def readExistingData(self):
         try:
            with open("./ExpenseTracker.json","r") as file:
                  data = json.load(file)
         except Exception as e:
            print("No Exisitng data")         
            self.expenses=[]
         else:
            for exp in data:
                 self.expenses.append(Expense(datetime.strptime(exp["date"],"%Y-%m-%d %H:%M:%S"),exp["category"],exp["amount"],exp["note"]))

    def writeExistingData(self):
        with open("./ExpenseTracker.json","w") as file:
            data=[]
            for exp in self.expenses:
                data.append({"date" : exp.date, "category" : exp.category , "amount" : exp.amount , "note" : exp.note })
            json.dump(data,file,indent=4,default=str)
              

    def addExpense(self,expense):
        self.expenses.append(expense)
    
    def removeExpense(self,index):
        if len(self.expenses) > 0 and index <= len(self.expenses):
            del self.expenses[index]
        else:
            print("Please provide valid index.")

    def listExpenses(self):
        if len(self.expenses) > 0 :
                print("List of Expenses")
                print("------------------------------------------------------------------------------------------------------------")
                ind = 0
                for exp in self.expenses:
                    ind = ind+1
                    print(f"| {ind} | Date:{exp.date} | Category : {exp.category} | Amount : {exp.amount} | Note : {exp.note} |")
                print("------------------------------------------------------------------------------------------------------------")
        else:
                print("There is No Expense.")
    
    def searchExpense(self,searchText):
         isItemMatch = False
         IsDateMonth = False
         try:
            parsedDate = datetime.strptime(searchText,"%Y-%m")
         except:
             IsDateMonth = False
         else:
             IsDateMonth = True
         if IsDateMonth:
            for exp in self.expenses:             
                if  exp.date.year == parsedDate.year and exp.date.month == parsedDate.month:
                    isItemMatch = True
                    print(f"| Date:{exp.date} | Category : {exp.category} | Amount : {exp.amount} | Note : {exp.amount} |")
                    
         else:
             for exp in self.expenses:
                if  searchText.lower()  in exp.category.lower():
                    isItemMatch = True
                    print(f"| Date:{exp.date} | Category : {exp.category} | Amount : {exp.amount} | Note : {exp.amount} |")
                    
         if not(isItemMatch):
              print("No match item found in expenses")
    
    def monthlySummary(self):
         summary={}
         for exp in self.expenses:
                if exp.category not in summary:
                     summary[exp.category] = { "expenses":[],"total":0,"count":0 }

                summary[exp.category]["expenses"].append(f"Date : {exp.date} | Category :  {exp.category} | Amount : {float(exp.amount)} | Note :  {exp.note}")
                summary[exp.category]["total"] = float(summary[exp.category]["total"]) + float(exp.amount)
                summary[exp.category]["count"] = int(summary[exp.category]["count"]) + 1
         
         labels=[]
         count=[]
         for cat in summary: 
              print(f"Category : {cat} ")
              print(f"Total Expense : {summary[cat]['total']}")
              labels.append(cat)
              count.append(summary[cat]["count"])
              for exp in summary[cat]["expenses"]:
                   print(f"{exp}")
        
         print(labels)
         print(count)
         fig, ax = plt.subplots()
         ax.pie(count, labels=labels, autopct='%1.1f%%')
         plt.show()

expManager = ExpenseManager()
expManager.readExistingData()
'''notification.notify(
    title="Expense Tracker",
    message="Expense Tracker is started",
    timeout=5
)'''
while True:
    print(Fore.LIGHTMAGENTA_EX)
    print("EXPENSE TRACKER")
    print("Please selct one of the below option :")
    print("______________________________________")
    print("1. Add Expense | 2. Remove Expense | 3. List Expenses | 4. Search Expenses | 5. Monthly Summary | E Exit")

    selectedOption = input("Please enter your option : ")
    print(Fore.RESET)
    if selectedOption == "1":
         print("Add Expense")
         while True:
            try:
                date = input("Please provide expense date : ")
                parsedDate = datetime.strptime(date, "%Y-%m-%d")
            except:
                print("Please enter valid date (YYYY-MM-DD)")
            else:
                break
        
         
         while True:
           category = input("Please select any category [Food, Travel, Grocerry, Medical, Courses]")
           if category in ["Food", "Travel", "Grocerry", "Medical", "Courses"]:
                break
           else:
                print("Please selct valid category")
         1
         while True:
            try:
                amount=float(input("Please enter expense amount : "))
            except Exception as e:
                print("Please enter valid amount")
            else:
                 break
         

         note = input("Please enter note : ")

         exp = Expense(parsedDate,category,amount,note)

         expManager.addExpense(exp)
           
         
    elif selectedOption == "2":
        print("Remove Expense")
        while True:
            try:
                ind = int(input(f"Please enter the index of expense to remove (Max : {len(expManager.expenses)} ): "))
            except Exception as e:
                print("Please enter valid index")
            else:
                expManager.removeExpense(ind-1)
                break
    elif selectedOption == "3":
        print("List Expenses")
        expManager.listExpenses()
    elif selectedOption == "4":
        print("Search Expenses")
        searchText = input("Please enter category or date to search the expense : ")
        expManager.searchExpense(searchText)
    elif selectedOption == "5":
        print("Monthly Summary")
        expManager.monthlySummary()
    elif selectedOption.lower() == "e":
        print("Exit")
        expManager.writeExistingData()
        break      
    else:
        print("Please choose valid option")   


