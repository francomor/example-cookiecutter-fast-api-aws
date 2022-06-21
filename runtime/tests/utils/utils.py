import random
import string

from runtime.src.core import config


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_superuser_token_headers(test_client):
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    response = test_client.post(
        f"{config.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # superuser_token_headers = headers
    return headers
