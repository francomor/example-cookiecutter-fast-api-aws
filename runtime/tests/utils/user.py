from runtime.src import crud
from runtime.src.core import config
from runtime.src.db.session import db_session
from runtime.src.models.user import UserCreate

from .utils import random_lower_string


def user_authentication_headers(test_client, email, password):
    data = {"username": email, "password": password}
    response = test_client.post(f"{config.API_V1_STR}/login/access-token", data=data)
    response = response.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user
