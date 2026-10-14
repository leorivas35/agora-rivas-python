import json

from django.test import Client


def test_create_user_via_api(client: Client) -> None:
    response = client.post(
        "/api/users",
        data=json.dumps({"name": "Bob", "email": "bob@example.com"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Bob"
    assert response.json()["email"] == "bob@example.com"


def test_create_user_rejects_invalid_email(client: Client) -> None:
    response = client.post(
        "/api/users",
        data=json.dumps({"name": "Bob", "email": "not-an-email"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_health_endpoint(client: Client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
