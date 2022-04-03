from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routers.vote import vote
# from .database import engine
# from . import models # Importing everything from a file
from .routers import post, user, auth, vote



# Creates all of our models -> Tells SQLAlchemy to generarte based on models
# We don't need this with Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Which domains/websites can use your API
# As a public API you can use a wildcard -> ["*"]
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Hello World!!"}

