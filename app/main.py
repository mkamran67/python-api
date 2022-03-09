from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


# Creates all of our models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Post class extends basemodel -> pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Defaulted to True


while True:
    # ORM Setup
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='peace123q', cursor_factory = RealDictCursor)
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

# Test
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data" : posts}

# db session must be passed in when you're 'tapping' into the db
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    # # fastapi will serialize this into JSON format
    # cursor.execute("""SELECT * FROM posts""")
    # # Runs the SQL Command
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return {"data": posts}

# pass status code 
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data":  new_post}

# For Demo
# @app.get("/posts/latest")
# def get_latest_posts():
#     latest = my_posts[len(my_posts)-1]
#     return {"detail": latest}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # type check with fastapi
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

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

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    

    return {"data" : updated_post}