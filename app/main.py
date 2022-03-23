from fastapi import FastAPI

from app.routers.vote import vote
from .database import engine
from . import models # Importing everything from a file
from .routers import post, user, auth, vote



# Creates all of our models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Hello World!"}

