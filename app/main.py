from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Post class extends basemodel -> pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Defaulted to True
    rating: Optional[int] = None


while True:
    # ORM Setup
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='silverberry', password='peace123q', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("DB Connected")
        break

    except Exception as error:
        print("Connecting to DB Failed")
        print("Error: ", error)
        time.sleep(5)


# temp posts container
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "FaveFruit", "content": "All things Kiwi and Pomegrante", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
def get_posts():
    # fastapi will serialize this into JSON format
    return {"data": my_posts}

# pass status code 
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000) # for dev purposes so id is uniq
    my_posts.append(post_dict)
    return {"data":  post_dict}

# For Demo
# @app.get("/posts/latest")
# def get_latest_posts():
#     latest = my_posts[len(my_posts)-1]
#     return {"detail": latest}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # type check with fastapi
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleteing post
    # finding the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID does not exist')

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data" : post_dict}