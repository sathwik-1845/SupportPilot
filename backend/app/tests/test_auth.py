import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-test-secret-key-0123456789")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app as fastapi_app
from app.models import user as _user_models  # noqa: F401

API = "/api/v1"
CREDS = {"email": "Test@Example.com", "password": "Passw0rd123"}


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(fastapi_app)  # no context manager: skips lifespan (no real Postgres needed)
    fastapi_app.dependency_overrides.clear()


def login(client, password="Passw0rd123"):
    return client.post(f"{API}/auth/login", data={"username": "test@example.com", "password": password})


def test_register_and_duplicate(client):
    r = client.post(f"{API}/auth/register", json=CREDS)
    assert r.status_code == 201
    assert r.json()["email"] == "test@example.com"  # normalized
    assert "password" not in r.text
    assert client.post(f"{API}/auth/register", json=CREDS).status_code == 409


@pytest.mark.parametrize(
    "body",
    [
        {"email": "not-an-email", "password": "Passw0rd123"},
        {"email": "a@b.com", "password": "short1"},
        {"email": "a@b.com", "password": "onlyletters"},
    ],
)
def test_register_validation(client, body):
    assert client.post(f"{API}/auth/register", json=body).status_code == 422


def test_login_failures_are_identical(client):
    client.post(f"{API}/auth/register", json=CREDS)
    wrong_pw = login(client, "WrongPass1")
    unknown = client.post(f"{API}/auth/login", data={"username": "no@one.com", "password": "x"})
    assert wrong_pw.status_code == unknown.status_code == 401
    assert wrong_pw.json() == unknown.json()


def test_protected_route_needs_token(client):
    assert client.get(f"{API}/auth/me").status_code == 401
    bad = client.get(f"{API}/auth/me", headers={"Authorization": "Bearer garbage"})
    assert bad.status_code == 401


def test_full_flow_with_logout(client):
    client.post(f"{API}/auth/register", json=CREDS)
    tok = login(client).json()["access_token"]
    h = {"Authorization": f"Bearer {tok}"}

    assert client.get(f"{API}/auth/me", headers=h).json()["email"] == "test@example.com"
    assert client.post(f"{API}/auth/logout", headers=h).status_code == 204
    assert client.get(f"{API}/auth/me", headers=h).status_code == 401  # revoked


def test_health_routes(client):
    assert client.get(f"{API}/health").json() == {"status": "ok"}
    assert client.get(f"{API}/health/db").json()["database"] == "connected"