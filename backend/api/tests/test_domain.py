import pytest
from fastapi.testclient import TestClient
from api import api
from api.db import db

db.init_app(api)

@pytest.fixture(scope="module")
def client():
    with TestClient(api) as c:
        yield c



def test_swagger_docs():
    api_client = client()
    response = api_client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_openapi(api_client):
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json().keys() == dict_keys(
        ["openapi", "info", "paths", "components"]
    )
