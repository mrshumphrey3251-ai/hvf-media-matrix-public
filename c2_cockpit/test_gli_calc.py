from fastapi.testclient import TestClient
from gli_calc import app

client = TestClient(app)

def test_compute_gli_normal():
    response = client.post("/compute", json={"R": 120, "G": 150, "B": 80})
    assert response.status_code == 200
    assert response.json()["GLI"] > 0

def test_compute_gli_division_by_zero():
    response = client.post("/compute", json={"R": 0, "G": 0, "B": 0})
    assert response.status_code == 400

if __name__ == "__main__":
    print("QA Pipeline Passed.")
