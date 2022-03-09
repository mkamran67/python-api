from multiprocessing import synchronize
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

# Post class extends basemodel -> pydantic -> Schema
# Schema/Pydantic model(s) define the structure of a request & response
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
def create_posts(post: Post, db: Session = Depends(get_db)):
    

    # cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(**post.dict())
    # Unpack the dictionary
    new_post = models.Post(**post.dict())

    db.add(new_post) # add post to
    db.commit() # commits entry to DB
    db.refresh(new_post) # Refreshes the new post variable with DB entry


    return {"data":  new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)): # type check with fastapi

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    # filter by id and get the first found
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleteing post

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    retrieved_post = post_query.first()

    if retrieved_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    #update requires a dictionary of updated materials
    post_query.update(post.dict(),synchronize_session=False)

    db.commit()

    return {"data" : post_query.first()}