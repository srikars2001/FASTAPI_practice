from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import *
from sqlalchemy.orm import Session
from ..database import engine,get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate ,db : Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_create_query = db.query(models.User).filter(models.User.email == user.email)

    if user_create_query.first() != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with email id : {user.email} exists")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemas.UserCreateResponse)
def get_user(id:int,db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} not found")

    return user    
    
