from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()
# Post class extens basemodel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Defaulted to True
    rating: Optional[int] = None


# temp posts container
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},{"title": "FaveFruit", "content": "All things Kiwi and Pomegrante", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
def get_posts():
    # fastapi will serialize this into JSON format
    return {"data": my_posts}

@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000) # for dev purposes so id is uniq
    my_posts.append(post_dict)
    return {"data":  post_dict}


@app.get("/posts/latest")
def get_latest_posts():
    latest = my_posts[len(my_posts)-1]
    return {"detail": latest}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # type check with fastapi
    post = find_post(id)

    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
    
    return {"post_details": post}
