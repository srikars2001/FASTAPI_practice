from fastapi import FastAPI
from fastapi.params import *
from . import models
from .database import engine
from .routers import post,user,auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"msg" : "welcome to my api"}
