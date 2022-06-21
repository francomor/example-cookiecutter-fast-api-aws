import pytest
from fastapi.testclient import TestClient

from runtime.src.main import app
from runtime.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def superuser_token_headers(test_client):
    return get_superuser_token_headers(test_client)
