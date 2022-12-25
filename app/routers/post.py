
from .. import models,schemas,utils,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import *
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/",response_model=List[schemas.Post])
async def get_posts(db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)): 
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #return {"data" : posts}
    print("@post.py get current user - >",current_user)
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)   
async def create_posts(post : schemas.PostCreate , db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title,
    #                post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #return {"data" : new_post}

    """ new_post = models.Post(title=post.title,
                content = post.content,
                published = post.published) """

    print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int , db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)) )
    #test_post = cursor.fetchone()

    test_post = db.query(models.Post).filter(models.Post.id == str(id)).first()

    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")

    return test_post

""" 
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i
    return None """

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    
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



@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate , db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    
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

    return post_query.first()