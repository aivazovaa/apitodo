import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_user_registration_and_token():
    resp = client.post("/users/", json={"username":"karina","password":"karinapass"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "karina"
    resp2 = client.post("/users/token", data={"username":"karina","password":"karinapass"})
    assert resp2.status_code == 200
    tok = resp2.json()
    assert "access_token" in tok

def test_task_crud():
    client.post("/users/", json={"username":"karina","password":"karinapass"})
    tok = client.post("/users/token", data={"username":"karina","password":"karinapass"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {tok}"}
    resp = client.post("/tasks/", json={"title":"T","description":"D"}, headers=headers)
    assert resp.status_code == 200
    task = resp.json()
    assert task["title"] == "T"
    tid = task["id"]
    resp2 = client.get("/tasks/", headers=headers)
    assert resp2.status_code == 200
    assert any(t["id"] == tid for t in resp2.json())
    resp3 = client.get(f"/tasks/{tid}", headers=headers)
    assert resp3.status_code == 200
    assert resp3.json()["id"] == tid
