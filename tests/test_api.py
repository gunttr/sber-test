from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app=app)

def test_client_ip_with_no_proxy():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["client_ip"] == "testclient"


def test_client_ip_with_proxy():
    response = client.get(
        "/",
        headers={"X-Forwarded-For": "5.6.7.8, 1.2.3.4, 9.8.1.3"}
    )

    assert response.status_code == 200
    assert response.json()["client_ip"] == "5.6.7.8"