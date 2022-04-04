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
from app.oauth2 import create_access_token
from app import models

# ---------------------- Testing DB setup ----------------------

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessionlocal object is responisble for talking to databases
sessionLocalForTests = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------- Fixures ----------------------
# Scope declaration when it's created and destroy
@pytest.fixture
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


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session

        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "testit1@test.com", "password": "123123q"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "testit2@test.com", "password": "123123q"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


# Gets an authenticated client
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "Wake Up, Ron Burgundy",
            "content": "Vivamus tortor. Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis.",
            "owner_id": test_user["id"],
        },
        {
            "title": "Sister Helen ",
            "content": "Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum.",
            "owner_id": test_user["id"],
        },
        {
            "title": "Soldier of Orange (a.k.a. Survival Run) (Soldaat van Oranje)",
            "content": "Nunc nisl.",
            "owner_id": test_user["id"],
        },
        {
            "title": "Urbanized",
            "content": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor.",
            "owner_id": test_user["id"],
        },
        {
            "title": "Illustrious Corpses (Cadaveri eccellenti)",
            "content": "Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus.",
            "owner_id": test_user2["id"],
        },
        {
            "title": "Father of the Bride",
            "content": "Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.",
            "owner_id": test_user2["id"],
        },
        {
            "title": "4:44 Last Day on Earth",
            "content": "Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui. Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo.",
            "owner_id": test_user2["id"],
        },
        {
            "title": "Whoopi Goldberg Presents Moms Mabley",
            "content": "Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio.",
            "owner_id": test_user2["id"],
        },
        {
            "title": "Three Worlds (Trois mondes)",
            "content": "Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor.",
            "owner_id": test_user2["id"],
        },
        {
            "title": "Eragon",
            "content": "Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus.",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    return session.query(models.Post).all()
