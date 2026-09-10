from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/fruits",tags=["fruits"])

items = [{"name":"mango"},{"name":"banana"}]

@router.get("/")
def getItems():
    return items

class Fruit(BaseModel):
    name:str

@router.post("/new",response_model=list[Fruit])
def createFruit(item:Fruit):
    items.append(item)
    return items