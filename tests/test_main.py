from fastapi.testclient import TestClient
from main import app  # Assuming main.py is the FastAPI app

client = TestClient(app)

# tests the FastAPI / route
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
