from runtime.src import crud
from runtime.src.core import config
from runtime.src.db.session import db_session
from runtime.src.models.user import UserCreate
from runtime.tests.utils.user import user_authentication_headers
from runtime.tests.utils.utils import random_lower_string


def test_get_users_superuser_me(test_client, superuser_token_headers):
    r = test_client.get(
        f"{config.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == config.FIRST_SUPERUSER


def test_create_user_new_email(test_client, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{config.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    assert username == created_user["email"]


def test_get_existing_user(test_client, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db_session, user_in=user_in)
    user_id = user.id
    r = test_client.get(
        f"{config.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    user = crud.user.get_by_email(db_session, email=username)
    assert user.email == api_user["email"]


def test_create_user_existing_username(test_client, superuser_token_headers):
    username = random_lower_string()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, user_in=user_in)
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{config.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(test_client):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, user_in=user_in)
    user_token_headers = user_authentication_headers(test_client, username, password)
    data = {"email": username, "password": password}
    r = test_client.post(
        f"{config.API_V1_STR}/users/", headers=user_token_headers, json=data
    )
    assert r.status_code == 400


def test_retrieve_users(test_client, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db_session, user_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db_session, user_in=user_in2)

    r = test_client.get(
        f"{config.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
