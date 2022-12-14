import time
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import *
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session
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

@app.get("/")
async def root():
    return {"msg" : "welcome to my api"}

@app.get("/posts")
async def get_posts(db : Session = Depends(get_db)): 
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #return {"data" : posts}
    posts = db.query(models.Post).all()
    return {"data" : posts} 


@app.post("/posts", status_code=status.HTTP_201_CREATED)   
async def create_posts(post : schemas.PostCreate    , db:Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,
    #                post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #return {"data" : new_post}

    """ new_post = models.Post(title=post.title,
                content = post.content,
                published = post.published) """
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id:int , db : Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)) )
    #test_post = cursor.fetchone()

    test_post = db.query(models.Post).filter(models.Post.id == str(id)).first()

    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")

    return {"post_detail": test_post}

""" 
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i
    return None """

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))

    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == str(id))
   
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id:int, updated_post:schemas.PostCreate , db:Session = Depends(get_db)):
    
    #cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id=%s RETURNING *""",
    #                (post.title,post.content,post.published,str(id),)) 
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return {"data" : post_query.first()}
