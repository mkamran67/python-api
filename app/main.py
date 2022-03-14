from typing import Optional, List
from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils # Importing everything from a file
from .routers import post, user, auth

# Creates all of our models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message" : "Hello World!"}

