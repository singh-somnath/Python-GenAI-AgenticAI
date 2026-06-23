'''
num= 101
if num%2 == 0 :
    print("Even")
else:
    print("Odd")


count =1
while count < 10:
    count+=1
    print(count)
        exit=input("Press e if you want to exit")
    if exit is not "":
        if exit[0] == "e":
            break
    
num=int(input("Please Enter a number : "))
isPrime=False
if num==1 or num == 2:
    print("prime")
else:
    for n in range(2,num-1):
        if num%n == 0:
            isPrime=False
            break
        else:
            isPrime=True
            continue
if isPrime == True:
    print("Prime Number")
else:
    print("Not a Prime Number")
    
numbers=[34,5,76,8,23,5,90,12,324,1,33]
print(numbers)

for i in range(0,len(numbers)):
    for j in range(0,len(numbers)-i-1):
        if numbers[j] > numbers[j+1]:
            temp = numbers[j]
            numbers[j] = numbers[j+1]
            numbers[j+1] = temp

print(numbers)

str=input("Enter a string : ")
lastIndex = len(str)-1
isPlaindrom = True
for i in range(0,int(len(str)/2)):
    if str[i].lower() != str[lastIndex].lower():
        isPlaindrom = False
        break
    lastIndex-=1
if isPlaindrom:
    print("Palindrom")
else:
    print("Not Palindrom")
#################################################################
try:
    num = int(input("Please enter number : "))
except Exception as e:
    print("Please enter a valid positive number")
else:
    if num < 1 :
        print("Please enter a positive number")
    else:
        factValue=1
        for n in range(1,num+1):
            factValue = factValue * n
        
        print("Factorial Value : ", factValue)
####################################################################

####################################################################
def checkNumber(num):
    if num%2 == 0:
        return "Even"
    else:
        return "Odd"

print(checkNumber(8))
####################################################################
'''
import csv
with open("./NumbersAddition.csv","r") as file:
    reader = csv.reader(file)
    header = next(reader)
    dataRows = list(reader)

AdditionIndex = header.index("Result")

for row in dataRows:
    num1=row[header.index("Number 1")]
    num2=row[header.index("Number 2")]
    sum = float(num1) + float(num2)
    row[AdditionIndex] = f"{sum}"
    
with open("./NumbersAddition.csv","w",newline="") as outfile:
     wr = csv.writer(outfile)
     wr.writerow(header)
     wr.writerows(dataRows)

with open("./NumbersAddition.csv","r") as file:
     print(file.read())
    




            
