from fastapi.testclient import TestClient

from agora_rivas.main import app


client = TestClient(app)


def test_create_user_via_api() -> None:
    response = client.post(
        "/api/users",
        json={"name": "Bob", "email": "bob@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Bob"
    assert response.json()["email"] == "bob@example.com"
