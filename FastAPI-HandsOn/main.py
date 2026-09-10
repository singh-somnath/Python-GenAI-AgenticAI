from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel, Field

from app.router import fruits

app = FastAPI(title="My API",version="1.0.0.0")

@app.get("/")
def root():
    return ({"message":"Welcome to Fast API"}) 

@app.get("/health")
def health():
    return ({"status":"ok"})



class Item(BaseModel):
    name:str
    description : str
    price:float= Field(gt=0, description="This must be positive value")
    tax:float = Field(gt=-1, description="This must be positive value")

@app.post("/item/")
def createItem(item:Item):
    totalPrice = item.price + item.tax
    return { "Price" : item.price, "Price_with_tax" : totalPrice}

#############Response Model and Status Code

class userIN(BaseModel):
    username:str
    password:str

class userOUT(BaseModel):
    username:str

@app.post("/user/",response_model=userOUT,status_code=status.HTTP_201_CREATED)
def userCreate(user:userIN):
    return user

###HTTPException

db = {"1":"Test Data"}

@app.get("/items/{item_id}")
def read_item(item_id:int,q:str="NA",active:bool=True):
    if str(item_id) not in db:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Item not found")
    
    if q.lower()=="na":
        return {"message":f"Item- {item_id} | Active - {active}"}
    else:
        return {"message":f"Item - {item_id} | query - {q} |Active - {active}"}

###Dependency Injection

db = {
    "user":"somnath",
    "type":"admin   "
} 

def getCurrentUSer():
    if db.get("type") != "admin" :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User has no access")

@app.patch("/item/{item_id}",dependencies=[Depends(getCurrentUSer)])
def updateItem(item_id : int):
    return {"status":"Item has updated"}


#####
app.include_router(fruits.router)




