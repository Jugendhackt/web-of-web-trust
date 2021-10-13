from fastapi.testclient import TestClient
from api import api
from api.db import db

db.init_app(api)
client = TestClient(api)


def test_swagger_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json().keys() == dict_keys(
        ["openapi", "info", "paths", "components"]
    )
