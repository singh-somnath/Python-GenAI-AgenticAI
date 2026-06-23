from colorama import Fore,Back,Style
import csv
import json
#####################################################################################################################################
#Book
class Book:
    def __init__(self,name,author,year,status="available"):
        self.name=name
        self.author=author
        self.year=year
        self.status=status
    
    def borrow_book(self):
        if self.status == "available":
            self.status = "borrowed"
        elif self.status == "borrowed":
            print("Already Borrowed")
    
    def return_book(self):
        if self.status == "borrowed":
            self.status="available"
    
    def details(self):
        print(Fore.BLUE)
        print(f"| Book Name : {self.name} |")
        print(f"| Book Author : {self.author} |")
        print(f"| Published Year : {self.year} |")
        print(f"| Book Status : {self.status} |")
        print(Fore.RESET)


######################################################################################################################################
#Library
class Library:
    def __init__(self):
        self.books = []
        self.header = None

    def readFile(self):
        self.readJSON()

    def readCSV(self):
        print("Reading CSV...")
        try:
            with open("./libraryManagement.csv","r") as file:
                reader = csv.reader(file)
                self.header = next(reader)
                datarows = list(reader)
        except Exception as e:
            print("Issue with csv")
            self.books = []
        else:          
            for bk in datarows:
                self.books.append(Book(bk[self.header.index("name")],bk[self.header.index("author")],bk[self.header.index("year")],bk[self.header.index("status")]))

    def readJSON(self):
        try:
            with open("./libraryManagement.json","r") as file:
                data = json.load(file)
        except Exception as e:
            self.books=[]
        else:
            for bk in data:
                self.books.append(Book(bk["name"],bk["author"],bk["year"],bk["status"]))


    def writeFile(self):
        self.writeJSON()
    
    def writeCSV(self):
        with open("./libraryManagement.csv","w",newline="") as file:
                writer = csv.writer(file)
                if self.header != None:
                    writer.writerow(self.header)
                if len(self.books) > 0 :
                    for bk in self.books:
                        writer.writerow([bk.name,bk.author,bk.year,bk.status])
    
    def writeJSON(self):
        with open("./libraryManagement.json","w") as file:
            data=[]
            for bk in self.books:
                data.append({"name":bk.name,"author":bk.author,"year":bk.year,"status":bk.status})
            json.dump(data,file,indent=4)


    def addNewBook(self,book):
        self.books.append(book)
    
    def removeBook(self,name):
        for bk in self.books:
            if bk.name.lower() == name.lower():
                self.books.remove(bk)

    def boorowBook(self,title):
        bookFound = False
       
        for bk in self.books:
            if bk.name.lower() == title.lower():
                bk.borrow_book()
                bookFound = True
                break

        if bookFound != True:
            print("Invalid Book Detail")


    def returnBook(self,title):
        bookFound = False
        for bk in self.books:
            if bk.name.lower() == title.lower():
                bk.return_book()
                bookFound = True
                break
        
        if bookFound != True:
            print("Invalid Book Detail")


    def serachBookByAuthorTitle(self,serachText):
        isBookFound = False
        for bk in self.books:
            if serachText.lower() in bk.name.lower() or serachText.lower() in bk.author.lower():
                findBook = bk
                isBookFound=True
                break
        
        if isBookFound == True:
            return findBook
        else:
            return None
        
    def listAllBooks(self):        
        if len(self.books) < 1:
            print("No Books Available")
            return
        for bk in self.books:
            print(Fore.BLUE)
            print(f"Book Title : {bk.name} | Status : {bk.status}" )
        print(Fore.RESET)
#####################################################################################################################333
#Main
library = Library()
library.readFile()

while True:
   
    print(Fore.GREEN,"Please selct one of the below option :")
    print("______________________________________")
    print("1 Add Book | 2 Remove Book | 3 Borrow Book | 4 Return Book | 5 Search Book | 6 List All Book | E Exit")

    print(Fore.MAGENTA)
    selectedOption = input("Enter your option : ")
    print(Fore.YELLOW)
    if selectedOption != None and selectedOption.lower() == "e":
       library.writeFile()
       break
    elif selectedOption == "1":
        print("Give Book Details")
        name=input("Book Name : ")
        author=input("Book Author : ")
        year=input("Published Year : ")

        book = Book(name,author,year)
        library.addNewBook(book)
        print("------------------------------------------------------------------------")
    elif selectedOption == "2":
        name = input("Give Book Name : ")
        print("------------------------------------------------------------------------")
        library.removeBook(name)
        print("------------------------------------------------------------------------")
    elif selectedOption == "3":
        print("------------------------------------------------------------------------")
        name = input("Give Book Name : ")
        print("------------------------------------------------------------------------")
        library.boorowBook(name)
        print("------------------------------------------------------------------------")
    elif selectedOption == "4":
        print("------------------------------------------------------------------------")
        name = input("Give Book Name : ")
        library.returnBook(name)
        print("------------------------------------------------------------------------")
    elif selectedOption == "5":
        print("------------------------------------------------------------------------")
        name = input("Give Book Name/Title : ")
        book = library.serachBookByAuthorTitle(name)
        book.details()
        print("------------------------------------------------------------------------")
    elif selectedOption == "6":
        print("------------------------------------------------------------------------")
        library.listAllBooks()
        print("------------------------------------------------------------------------")
    else:
        print(Fore.RED,"Please Enter valid option.",Fore.RESET)

Fore.RESET
