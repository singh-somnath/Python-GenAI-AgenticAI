'''
import random
# First let's create some things:

fruits = ["Apples", "Bananas", "Pears","Pearst"]

book1 = {"title": "Great Expectations", "author": "Charles Dickens"}
book2 = {"title": "Bleak House", "author": "Charles Dickens"}
book3 = {"title": "An Book By No Author"}
book4 = {"title": "Moby Dick", "author": "Herman Melville"}

print(random.choice(fruits))

books =[book1,book2,book3,book4]
'''
for k in range(1,10,2):
    print(k)
#print(books[2]["author"])
'''
for k in books[2]:
    print(k)
print("title" in books[2])

print([fr.get("title") for fr in books if fr.get("author")])

print(books[2].get("author"))

def listNumbers(n):
    for i in range(0,n):
        yield i

nums = listNumbers(15)
for i in nums:
    print(i)
'''