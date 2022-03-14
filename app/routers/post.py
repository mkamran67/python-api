from app import oauth2
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# db session must be passed in when you're 'tapping' into the db
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # # fastapi will serialize this into JSON format
    # cursor.execute("""SELECT * FROM posts""")
    # # Runs the SQL Command
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts

# pass status code 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    
    print(user_id)

    # cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(**post.dict())
    # Unpack the dictionary
    new_post = models.Post(**post.dict())

    db.add(new_post) # add post to
    db.commit() # commits entry to DB
    db.refresh(new_post) # Refreshes the new post variable with DB entry


    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)): # type check with fastapi

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    # filter by id and get the first found
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    # deleteing post

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    retrieved_post = post_query.first()

    if retrieved_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    #update requires a dictionary of updated materials
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()
