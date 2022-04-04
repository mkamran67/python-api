from app import schemas
from jose import jwt
from app.config import settings
import pytest


# ------------------------------- Testing Start ------------------------------ #


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "testit2@test.com", "password": "123123q"}
    )
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201  # Created
    assert new_user.email == "testit2@test.com"


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    assert login_res.token_type == "bearer"

    # Validate the token
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")
    assert id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@test.com", "123123q", 403),
        ("testit2@test.com", "wrongpassowrd", 403),
        ("wrongemail@test.com", "wrongpassowrd", 403),
        ("testit2@test.com", "123123q", 200),
        (None, "123123q", 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    if res.status_code == 403:
        assert res.json().get("detail") == "Invalid Credentials"
    else:
        assert res.status_code == status_code
