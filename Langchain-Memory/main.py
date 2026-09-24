from src.NoMemory00 import chatAPP
from src.BasicMemory import chatAPP
from src.SummaryMemory import chatAPP
from src.TokenBufferMemory import chatAPP

def main():
    print("Hello from langchain-memory!")


a = lambda _ : "Hello"
b = lambda x : "Hello" + x 

n=['$1','$2','$56']

n1 = list(map(lambda a : float(a.replace('$','')) , n ))



if __name__ == "__main__":
    #chatAPP()
    print("main--->")
    print(a(9))
    print(b("world"))
    print(n1)

