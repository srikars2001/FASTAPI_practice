
from .. import models,schemas,utils,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import *
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine,get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit:int = 10,skip:int = 0,search: Optional[str] = ""): 
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #return {"data" : posts}
    #print(search)
    #print("@post.py get current user - >",current_user)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(posts)
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

    #print("in post.py ==> current user = ",current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int , db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)) )
    #test_post = cursor.fetchone()

    test_post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == str(id)).first()

    #test_post = db.query(models.Post).filter(models.Post.id == str(id)).first()

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

    deleted_post_query = db.query(models.Post).filter(models.Post.id == str(id))
    deleted_post = deleted_post_query.first()
   
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")
    
    if (deleted_post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    
    deleted_post_query.delete(synchronize_session=False)
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
    
    if (post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()