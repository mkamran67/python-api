from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr


# Post class extends basemodel -> pydantic -> Schema
# Schema/Pydantic model(s) define the structure of a request & response


# This is base model 'duh'
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # Defaulted to True

# This handles user sending us data
class PostCreate(PostBase):
    pass


# This handles us sending data to user
class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True # This lets pydantic know it's an orm model not a dictionary

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True # This lets pydantic know it's an orm model not a dictionary


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

