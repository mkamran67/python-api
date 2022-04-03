from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# Below in comments are various ways of importing environment variables
# import os
# from dotenv import load_dotenv
# from operator import itemgetter

# load_dotenv()

#environment variables - Using built in library itemgetter to destructer
# ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM = itemgetter('ACCESS_TOKEN_EXPIRE_MINUTES','SECRET_KEY','ALGORITHM')(os.environ)

# ACCESS_TOKEN_EXPIRE_MINUTES  = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']
# SECRET_KEY = os.environ['SECRET_KEY']
# ALGORITHM = os.environ['ALGORITHM']

ACCESS_TOKEN_EXPIRE_MINUTES  = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm



# feed the end point
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pieces of information that are needed
# 1. Secret Key
# 2. Algorithm we want to use -> HS256
# 3. Expiration time of the token

# Command below for generating random key
# openssl rand -hex 32


def create_access_token(data: dict):
    to_encode = data.copy() # Make a copy of data so we don't manipulate the original

    # Expiration should be UTC
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # data to encode, the secret, algorithm NOTE enocded_jwt algorithm vs payload algorithms
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
