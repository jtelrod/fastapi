from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

from starlette.status import HTTP_201_CREATED

app = FastAPI()

class Post(BaseModel):
 title: str
 content: str
 published: bool = True
 rating: Optional[int] = None

my_posts = [{"title": "title of post1", "content": "content of post1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
 for p in my_posts:
  if p["id"] == id:
   return p

def find_index_posts(id):
 for i, p in enumerate(my_posts):
  if p["id"] == id:
   return i

@app.get("/")
async def root_path():
 return {"message": "Hello"}

@app.get("/posts")
async def get_posts():
 return {"data": my_posts}

#orig
#@app.post("/createposts")
#async def create_posts(payLoad: dict = Body(...)):
# print(payLoad)
# return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}
@app.post("/posts", status_code=HTTP_201_CREATED)
async def create_posts(post: Post):
 print(post)
 print(post.dict())
 post_dict = post.dict()
 post_dict['id'] = randrange(0, 1000000)
 my_posts.append(post_dict)
 return {"data": post_dict}


@app.get("/posts/{id}")
async def get_post(id: int):
 post = find_post(id)
 if not post:
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                       detail=f"post with id: {id} was not found")
  # response.status_code = status.HTTP_404_NOT_FOUND
  # return {"message": f"post with id: {id} was not found"}
 return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
 index = find_index_posts(id)

 if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
 my_posts.pop(index)
 #return {"message": f"post {id} was successfully deleted"}
 return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
   print(post)
   index = find_index_posts(id)
   print(id)
   print(index)

   if index == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

   post_dict = post.dict()
   post_dict["id"] = id
   my_posts[index] = post_dict

   #my_posts
   return {"data": post_dict}