import time
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import *
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

my_posts = [
                {
                    "title" : "this is title",
                    "content" : "dirst post",
                    "id" : 1 
                },

                {
                    "title" : "sefcond post",
                    "content" : "hellow orls",
                    "id" : 2 
                }
            
            ]

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    #rating : Optional[int] = None
    
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

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
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)   
async def create_posts(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,
                    post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id:int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)) )
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")
    return {"post_detail": test_post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i
    return None

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    
    cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id=%s RETURNING *""",
                    (post.title,post.content,post.published,str(id),)) 
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")

    return {"data" : updated_post}

