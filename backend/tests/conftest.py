import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-test-secret-key-0123456789")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import get_db
from app.main import app as fastapi_app
from app.models import tenant as _t  # noqa: F401
from app.models.user import Role, User

API = "/api/v1"
PASSWORD = "Passw0rd123"


@pytest.fixture()
def session_factory():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(fastapi_app)  # no context manager -> no real Postgres needed
    fastapi_app.dependency_overrides.clear()


def register_business(client, name="Acme", admin_email="admin@acme.com", business_email=None):
    r = client.post(
        f"{API}/auth/register-business",
        json={
            "business_name": name,
            "business_email": business_email or f"hello@{name.lower()}.com",
            "industry": "Retail",
            "admin_full_name": f"{name} Admin",
            "admin_email": admin_email,
            "password": PASSWORD,
        },
    )
    assert r.status_code == 201, r.text
    return r.json()


def auth_headers(client, email, password=PASSWORD):
    r = client.post(f"{API}/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def add_agent(client, headers, email, role="support_agent"):
    r = client.post(
        f"{API}/users",
        headers=headers,
        json={"full_name": "Some Agent", "email": email, "password": PASSWORD, "role": role},
    )
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture()
def make_super_admin(session_factory):
    def _make(email="root@supportpilot.io"):
        with session_factory() as db:
            db.add(
                User(
                    tenant_id=None,
                    full_name="Root",
                    email=email,
                    hashed_password=get_password_hash(PASSWORD),
                    role=Role.SUPER_ADMIN,
                )
            )
            db.commit()
        return email

    return _make