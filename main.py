from enum import Enum
from typing import Optional, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]
latest_idx = 1


@app.get('/')
def root():
    return {"message": "Successful Response"}

@app.post('/post', summary="Get Post", operation_id="get_post_post_post")
def post():
    global latest_idx
    new_idx = latest_idx + 1
    latest_idx += 1

    new_timestamp = Timestamp(id=new_idx, timestamp=int(datetime.datetime.now().timestamp()))
    post_db.append(new_timestamp)
    return new_timestamp

@app.get('/dog')
def get_dogs(kind: Optional[Union[str, None]] = None):
    
    
    if kind is not None:
        if not kind in DogType.__dict__:
            raise HTTPException(status_code=422, detail={"loc": "dog kind", "msg": "dog kind {} is not supported".format(kind), "type": "KeyError"})

        res = [dog for idx, dog in dogs_db.items() if dog.kind == kind]
    else:
        
        res = [dog for idx, dog in dogs_db.items()]
    return res

@app.post('/dog')
def post_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=422, detail={"loc": "dogs_db", "msg": "dog idx is already in db".format(dog.pk), "type": "IDError"})

    dogs_db[dog.pk] = dog

    return dog

@app.get('/dog/{pk}')
def get_dogbyid(pk: int):
    
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=422, detail={"loc": "dogs_db", "msg": "no dog with id {} found".format(pk), "type": "IDError"})
    
    dog = dogs_db[pk]
    return dog

@app.patch('/dog/{pk}')  
def update_dog(pk: int, dog: Dog):
    
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=422, detail={"loc": "dogs_db", "msg": "no dog with id {} found".format(pk), "type": "IDError"})
    
    dogs_db[pk] = dog
   
    return dog