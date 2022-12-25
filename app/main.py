import time
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import *
from pydantic import BaseModel
from random import randrange
from typing import List,Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session

from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='srikar',
                                password='srikars@2001888648512',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database conn was succesfull")
        break

    except Exception as error:
        print("failed to connect to db")
        print("Error : ",error)
        time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"msg" : "welcome to my api"}
