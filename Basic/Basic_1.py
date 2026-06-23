import sys
greeting="Heloo Somnath"
greetin2="Heloo Somnath"
print(greeting + ", I am here.")
print("*"*9)
print(greeting,greetin2)

print(f"Hey : {greeting}")
text="Scientific Games!"
print(text[1:10])
print(text[9:])

print(text[9:].lower())
print(text.count('i'))
print(text.replace("Scientific","Squid"))
print(len(text))

test="HelloIndia2"
print(len(test))
print(test)
print(test.strip())
print(test.rstrip())

print(test.isalnum())
print(test.isalpha())

num1=5
num2=".5"

num3=num1+float(num2)
print(type(num2))
print(num3)
print(type(num3))

list=["Apple","Mango","Lemon","Pears",5,5.5,True]
print(list)
print(list[0])
print(list[-1])
print(list)
print(type(list[-1]))
list.append(3.14)
print(list)
list.insert(4,"somnath Singh")
print(list)
del list[6]
print(list)

text=""
listTest=["Apple","Mango","Lemon","Pears"]
print(text.join(listTest))

tp=("Apple","Mango","Lemon","Pears")
print(tp[-1])

tset={"apple","banana","orange","mango","pears","pears"}
print(tset)
print(hash("apple"));
print(hash("banana"));
print(hash("orange"));
print(hash("mango"));
print(hash("pears"));

num1=10
num2=6
print(num1%num2)