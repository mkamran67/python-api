from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection link
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:peace123q@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessionlocal object is responisble for talking to databases
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All models will be extending this base class
Base = declarative_base()