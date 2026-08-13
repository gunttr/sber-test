from redis import Redis
from fastapi.testclient import TestClient
from src.main import app

test_client = TestClient(app=app)
redis = Redis(host="localhost", port=6379, decode_responses=True)

def test_redis():
    response = test_client.get(
        "/",
        params={"client_hostname": "mypc"}
    )

    assert response.status_code == 200
    assert response.json()["client_ip"] == "testclient"
    assert redis.get("mypc") == "testclient"