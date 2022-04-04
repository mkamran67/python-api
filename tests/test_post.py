from venv import create
import pytest
from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    assert res.status_code == 200

    def validate_post(post):
        return schemas.PostOut(**post)

    # valid_posts = list(map(validate_post, res.json())) # Not in use, iteration over list

    assert len(res.json()) == len(test_posts)


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    # print(res.json())

    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_that_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/1337")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 200

    post = res.json()

    valid_post = schemas.PostOut(**post)

    assert valid_post.Post.id == test_posts[0].id


@pytest.mark.parametrize(
    "title, content, published, expected_code",
    [
        ("title 1", None, False, 422),
        (None, "Some content", False, 422),
        ("First valid post", "First valid post content", True, 201),
        ("", "Invalid owner content", False, 201),
    ],
)
def test_create_a_post(
    authorized_client, test_user, title, content, published, expected_code
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    # created_post = schemas.Post(**res.json())
    assert expected_code == res.status_code


@pytest.mark.parametrize(
    "title, content, published, expected_code",
    [
        ("title 1", None, False, 401),
        (None, "Some content", False, 401),
        ("First valid post", "First valid post content", True, 401),
        ("", "Invalid owner content", False, 401),
    ],
)
def test_unauthorized_user_create_a_post(
    client, test_user, title, content, published, expected_code
):
    res = client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    # created_post = schemas.Post(**res.json())
    assert expected_code == res.status_code


def test_unauthorized_user_delete_a_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    # print(res.json())

    # created_post = schemas.Post(**res.json())
    assert 401 == res.status_code


def test_authorized_user_delete_a_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert 204 == res.status_code


def test_authorized_user_delete_nonexisting_post(
    authorized_client, test_user, test_posts
):
    res = authorized_client.delete("/posts/1337")

    assert 404 == res.status_code


def test_delete_otherUser_post(authorized_client, test_user, test_posts, test_user2):
    res = authorized_client.delete("/posts/5")

    assert 403 == res.status_code


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200


def test_authorized_otherUser_update_post(
    authorized_client, test_user, test_user2, test_posts
):
    data = {
        "title": "updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[5].id}", json=data)

    assert res.status_code == 403
    # updated_post = schemas.Post(**res.json())


def test_Unauthorized_otherUser_update_post(client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }

    res = client.put(f"/posts/{test_posts[5].id}", json=data)

    assert res.status_code == 401
    # updated_post = schemas.Post(**res.json())


def test_Unauthorized_otherUser_update_post(client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "Updated content",
        "id": test_posts[0].id,
    }

    res = client.put("/posts/1337", json=data)

    assert res.status_code == 401
    # updated_post = schemas.Post(**res.json())
