import pytest

from tests.conftest import API, PASSWORD, add_agent, auth_headers, register_business


def body(**patch):
    b = {
        "business_name": "Acme", "business_email": "hello@acme.com", "industry": "Retail",
        "description": "We sell anvils.", "website_url": "acme.com",
        "admin_full_name": "Acme Admin", "admin_email": "admin@acme.com", "password": PASSWORD,
    }
    b.update(patch)
    return b


def test_register_stores_description_and_normalized_website(client):
    r = client.post(f"{API}/auth/register-business", json=body())
    assert r.status_code == 201
    t = r.json()["tenant"]
    assert t["description"] == "We sell anvils."
    assert t["website_url"] == "https://acme.com/"


def test_description_and_website_are_optional(client):
    b = body(website_url="", description=None)
    t = client.post(f"{API}/auth/register-business", json=b).json()["tenant"]
    assert t["website_url"] is None and t["description"] is None


@pytest.mark.parametrize("bad", ["not a url", "ftp://acme.com", "javascript:alert(1)", "http://"])
def test_invalid_website_rejected(client, bad):
    assert client.post(f"{API}/auth/register-business", json=body(website_url=bad)).status_code == 422


def test_admin_updates_own_business_profile(client):
    register_business(client, "Acme", "admin@acme.com")
    h = auth_headers(client, "admin@acme.com")
    r = client.patch(
        f"{API}/tenants/me", headers=h,
        json={"business_name": "Acme Corp", "industry": "Hardware", "description": "New text", "website_url": "https://acme.io"},
    )
    assert r.status_code == 200
    got = client.get(f"{API}/tenants/me", headers=h).json()
    assert (got["business_name"], got["industry"], got["description"]) == ("Acme Corp", "Hardware", "New text")
    assert got["website_url"] == "https://acme.io/"
    assert got["business_email"] == "hello@acme.com"  # untouched fields stay


def test_patch_only_affects_own_tenant(client):
    a = register_business(client, "Acme", "admin@acme.com")
    b = register_business(client, "Globex", "admin@globex.com")
    ha = auth_headers(client, "admin@acme.com")
    hb = auth_headers(client, "admin@globex.com")
    client.patch(f"{API}/tenants/me", headers=ha, json={"business_name": "Changed"})
    assert client.get(f"{API}/tenants/me", headers=hb).json()["business_name"] == "Globex"


def test_agent_cannot_edit_business_profile(client):
    register_business(client, "Acme", "admin@acme.com")
    add_agent(client, auth_headers(client, "admin@acme.com"), "agent@acme.com")
    h = auth_headers(client, "agent@acme.com")
    assert client.patch(f"{API}/tenants/me", headers=h, json={"business_name": "Hacked"}).status_code == 403


@pytest.mark.parametrize("patch", [{"status": "suspended"}, {"id": "x"}, {"tenant_id": "x"}])
def test_patch_cannot_touch_protected_fields(client, patch):
    register_business(client, "Acme", "admin@acme.com")
    h = auth_headers(client, "admin@acme.com")
    assert client.patch(f"{API}/tenants/me", headers=h, json=patch).status_code == 422


def test_patch_conflicts_and_nulls(client):
    register_business(client, "Acme", "admin@acme.com")
    register_business(client, "Globex", "admin@globex.com")
    h = auth_headers(client, "admin@acme.com")
    assert client.patch(f"{API}/tenants/me", headers=h, json={"business_email": "hello@globex.com"}).status_code == 409
    assert client.patch(f"{API}/tenants/me", headers=h, json={"business_name": None}).status_code == 422
    # same email as own current one is fine
    assert client.patch(f"{API}/tenants/me", headers=h, json={"business_email": "HELLO@acme.com"}).status_code == 200