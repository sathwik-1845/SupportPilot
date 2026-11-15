import pytest

from tests.conftest import API, PASSWORD, auth_headers, register_business


def test_register_business_creates_tenant_and_admin(client):
    data = register_business(client, "Acme", "Admin@Acme.com")
    assert data["user"]["email"] == "admin@acme.com"  # normalized
    assert data["user"]["role"] == "business_admin"
    assert data["user"]["tenant_id"] == data["tenant"]["id"]
    assert data["tenant"]["status"] == "active"
    assert "password" not in str(data)


def test_duplicate_emails_rejected(client):
    register_business(client, "Acme", "admin@acme.com")
    body = {
        "business_name": "Other", "business_email": "hello@acme.com", "industry": "Tech",
        "admin_full_name": "Someone", "admin_email": "new@other.com", "password": PASSWORD,
    }
    assert client.post(f"{API}/auth/register-business", json=body).status_code == 409  # business email
    body.update(business_email="hello@other.com", admin_email="admin@acme.com")
    assert client.post(f"{API}/auth/register-business", json=body).status_code == 409  # admin email


@pytest.mark.parametrize(
    "patch",
    [
        {"admin_email": "not-an-email"},
        {"password": "short1"},
        {"password": "onlyletters"},
        {"business_name": ""},
        {"role": "super_admin"},       # unknown field -> rejected
        {"tenant_id": "anything"},     # unknown field -> rejected
    ],
)
def test_register_business_validation(client, patch):
    body = {
        "business_name": "Acme", "business_email": "hello@acme.com", "industry": "Retail",
        "admin_full_name": "Admin", "admin_email": "admin@acme.com", "password": PASSWORD,
    }
    body.update(patch)
    assert client.post(f"{API}/auth/register-business", json=body).status_code == 422


def test_login_failures_are_identical(client):
    register_business(client)
    wrong = client.post(f"{API}/auth/login", data={"username": "admin@acme.com", "password": "WrongPass1"})
    unknown = client.post(f"{API}/auth/login", data={"username": "no@one.com", "password": "x"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_protected_route_needs_token(client):
    assert client.get(f"{API}/auth/me").status_code == 401
    assert client.get(f"{API}/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_me_and_logout(client):
    register_business(client)
    h = auth_headers(client, "admin@acme.com")
    me = client.get(f"{API}/auth/me", headers=h).json()
    assert me["email"] == "admin@acme.com" and me["role"] == "business_admin"
    assert client.post(f"{API}/auth/logout", headers=h).status_code == 204
    assert client.get(f"{API}/auth/me", headers=h).status_code == 401  # revoked


def test_health_routes(client):
    assert client.get(f"{API}/health").json() == {"status": "ok"}
    assert client.get(f"{API}/health/db").json()["database"] == "connected"