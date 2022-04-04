import pytest
from app import models


@pytest.fixture
def add_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user["id"])

    session.add(new_vote)

    session.commit()


def test_vote_on_post(authorized_client, test_posts):

    res = authorized_client.post(
        f"/vote/", json={"post_id": test_posts[0].id, "dir": 1}
    )

    # print(res.json())

    assert res.status_code == 201
    # updated_post = schemas.Post(**res.json())


def test_vote_on_unauthorized_post(client, test_posts):

    res = client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    # print(res.json())

    assert res.status_code == 401
    # updated_post = schemas.Post(**res.json())


def test_duplicate_vote_post(authorized_client, test_posts, add_vote):

    res = authorized_client.post(
        f"/vote/", json={"post_id": test_posts[0].id, "dir": 1}
    )

    assert res.status_code == 409


def test_delete_vote_post(authorized_client, test_posts, add_vote):

    res = authorized_client.post(
        f"/vote/", json={"post_id": test_posts[0].id, "dir": 0}
    )

    assert res.status_code == 201


def test_delete_vote_nonexist_post(authorized_client, test_posts):

    res = authorized_client.post(
        f"/vote/", json={"post_id": test_posts[0].id, "dir": 0}
    )

    assert res.status_code == 404


def test_vote_nonexisting_post(authorized_client, test_posts):

    res = authorized_client.post(f"/vote/", json={"post_id": 1337, "dir": 1})

    assert res.status_code == 404
