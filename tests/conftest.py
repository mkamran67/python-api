# Special file used by pytest
# Package specific fixtures from here will be avalible


import pytest
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ---------------------- Testing DB setup ----------------------

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessionlocal object is responisble for talking to databases
sessionLocalForTests = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------- Fixures ----------------------
# Scope declaration when it's created and destroy
@pytest.fixture(scope="module")
def session():

    # run our code after a test finishes -> Drop our tables
    Base.metadata.drop_all(bind=engine)
    # run our code before we run a test -> Create tables
    Base.metadata.create_all(bind=engine)

    db = sessionLocalForTests()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def test_user(client):
    user_data = {"email":"testit1@test.com", "password": "123123q"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data["password"]

    return new_user