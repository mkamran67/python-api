from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Below is another method of getting environment variables 
# import os
# from dotenv import load_dotenv
# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

# load_dotenv()
# SQLALCHEMY_DATABASE_URL = os.environ['SQLALCHEMY_DATABASE_URL'] # Environment variable


# connection link

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessionlocal object is responisble for talking to databases
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models will be extending this base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This is for raw SQL
# while True:
#     # ORM Setup
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='peace123q', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("DB Connected")
#         break

#     except Exception as error:
#         print("Connecting to DB Failed")
#         print("Error: ", error)
#         time.sleep(5)