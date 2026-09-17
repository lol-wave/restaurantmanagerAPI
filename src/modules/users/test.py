import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parents[3]))
sys.path.insert(0, str(Path(__file__).parents[2]))

from src.database import Base
from src.dependencies import get_current_user_id, get_db
from src.modules.restaurants.models import RestaurantModel
from src.modules.users.router import router


engine = create_engine(
	"sqlite://",
	connect_args={"check_same_thread": False},
	poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
	Base.metadata.create_all(bind=engine)
	app = FastAPI()
	app.include_router(router)

	def override_get_db():
		db = TestingSessionLocal()
		try:
			yield db
		finally:
			db.close()

	app.dependency_overrides[get_db] = override_get_db
	with TestClient(app) as test_client:
		yield test_client
	Base.metadata.drop_all(bind=engine)


def register_payload(username="alice"):
	return {
		"username": username,
		"email": f"{username}@example.com",
		"phone_number": "555-0100",
		"full_name": "Alice Example",
		"password": "correct-password",
		"password_confirm": "correct-password",
	}


def test_register_user(client):
	response = client.post("/register/", json=register_payload())

	assert response.status_code == 200
	body = response.json()
	assert body["username"] == "alice"
	assert body["email"] == "alice@example.com"
	assert "hashed_password" not in body


def test_register_rejects_duplicate_username(client):
	client.post("/register/", json=register_payload())

	response = client.post("/register/", json=register_payload())

	assert response.status_code == 400
	assert response.json()["detail"] == "Username or email already registered"


def test_register_rejects_mismatched_passwords(client):
	payload = register_payload()
	payload["password_confirm"] = "different-password"

	response = client.post("/register/", json=payload)

	assert response.status_code == 400
	assert response.json()["detail"] == "Passwords do not match"


def test_login_accepts_username_and_returns_token(client):
	client.post("/register/", json=register_payload())

	response = client.post(
		"/login/",
		json={"login": "alice", "password": "correct-password"},
	)

	assert response.status_code == 200
	body = response.json()
	assert body["user"]["username"] == "alice"
	assert body["tokens"]["token_type"] == "bearer"
	assert body["tokens"]["access_token"]


def test_login_rejects_unknown_user(client):
	response = client.post(
		"/login/",
		json={"login": "missing", "password": "correct-password"},
	)

	assert response.status_code == 404
	assert response.json()["detail"] == "Incorrect login or password!"


def test_get_user_requires_authentication(client):
	response = client.get("/users/1")

	assert response.status_code == 401


def test_authenticated_user_endpoints_return_user(client):
	registration = client.post("/register/", json=register_payload())
	user_id = registration.json()["id"]
	client.app.dependency_overrides[get_current_user_id] = lambda: user_id

	me_response = client.get("/me/")
	user_response = client.get(f"/users/{user_id}")

	assert me_response.status_code == 200
	assert user_response.status_code == 200
	assert me_response.json()["id"] == user_id
	assert user_response.json()["email"] == "alice@example.com"


def test_get_user_returns_not_found(client):
	client.app.dependency_overrides[get_current_user_id] = lambda: 1

	response = client.get("/users/999")

	assert response.status_code == 404
	assert response.json()["detail"] == "User not found"
