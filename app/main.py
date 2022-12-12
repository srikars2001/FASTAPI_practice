from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import *
from pydantic import BaseModel
from random import randrange

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
    rating : Optional[int] = None
    
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@app.get("/")
async def root():
    return {"msg" : "welcome to my api"}

@app.get("/posts")
async def get_posts():
    return {"data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)   
async def create_posts(post : Post):
    temp_post = post.dict()
    temp_post['id'] = randrange(3,100000000)
    my_posts.append(temp_post)
    return {"data" : temp_post}

@app.get("/posts/{id}")
def get_post(id:int):

    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found.")

    return {"post_detail": post}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i
    return None

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    post_index = find_index_post(id)
    if post_index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    
    post_index = find_index_post(id)
    if post_index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with post no {id} not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[post_index] = post_dict
    return {"data" : post_dict}

