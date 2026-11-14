from tests.conftest import API, add_agent, auth_headers, register_business


def two_tenants(client):
    a = register_business(client, "Acme", "admin@acme.com")
    b = register_business(client, "Globex", "admin@globex.com")
    return a, b, auth_headers(client, "admin@acme.com"), auth_headers(client, "admin@globex.com")


def test_list_users_only_returns_own_tenant(client):
    a, b, ha, hb = two_tenants(client)
    add_agent(client, ha, "agent1@acme.com")
    add_agent(client, hb, "agent1@globex.com")

    emails_a = {u["email"] for u in client.get(f"{API}/users", headers=ha).json()}
    emails_b = {u["email"] for u in client.get(f"{API}/users", headers=hb).json()}
    assert emails_a == {"admin@acme.com", "agent1@acme.com"}
    assert emails_b == {"admin@globex.com", "agent1@globex.com"}


def test_cannot_read_or_delete_other_tenants_user(client):
    a, b, ha, hb = two_tenants(client)
    victim = add_agent(client, hb, "victim@globex.com")

    assert client.get(f"{API}/users/{victim['id']}", headers=ha).status_code == 404
    assert client.delete(f"{API}/users/{victim['id']}", headers=ha).status_code == 404
    # still there, untouched
    assert client.get(f"{API}/users/{victim['id']}", headers=hb).status_code == 200


def test_tenant_id_cannot_be_supplied_by_client(client):
    a, b, ha, hb = two_tenants(client)
    r = client.post(
        f"{API}/users", headers=ha,
        json={"full_name": "Sneaky", "email": "s@acme.com", "password": "Passw0rd123", "tenant_id": b["tenant"]["id"]},
    )
    assert r.status_code == 422  # unknown field rejected
    created = add_agent(client, ha, "ok@acme.com")
    assert created["tenant_id"] == a["tenant"]["id"]  # always caller's tenant


def test_tenants_me_returns_own_tenant(client):
    a, b, ha, hb = two_tenants(client)
    assert client.get(f"{API}/tenants/me", headers=ha).json()["id"] == a["tenant"]["id"]
    assert client.get(f"{API}/tenants/me", headers=hb).json()["id"] == b["tenant"]["id"]


def test_role_permissions(client, make_super_admin):
    a, b, ha, hb = two_tenants(client)
    add_agent(client, ha, "agent@acme.com")
    h_agent = auth_headers(client, "agent@acme.com")

    # support agent: no user management, no admin area
    assert client.get(f"{API}/users", headers=h_agent).status_code == 403
    assert client.post(f"{API}/users", headers=h_agent, json={}).status_code in (403, 422)
    assert client.get(f"{API}/admin/tenants", headers=h_agent).status_code == 403
    assert client.get(f"{API}/tenants/me", headers=h_agent).status_code == 200
    # business admin: no super admin area
    assert client.get(f"{API}/admin/tenants", headers=ha).status_code == 403
    # super admin: has no tenant, so tenant-scoped user management is closed to it
    make_super_admin()
    hs = auth_headers(client, "root@supportpilot.io")
    assert client.get(f"{API}/users", headers=hs).status_code == 403
    assert client.get(f"{API}/tenants/me", headers=hs).status_code == 403


def test_cannot_create_super_admin_via_users_endpoint(client):
    a, b, ha, hb = two_tenants(client)
    r = client.post(
        f"{API}/users", headers=ha,
        json={"full_name": "Evil Admin", "email": "evil@acme.com", "password": "Passw0rd123", "role": "super_admin"},
    )
    assert r.status_code == 422


def test_admin_cannot_delete_self(client):
    a, b, ha, hb = two_tenants(client)
    assert client.delete(f"{API}/users/{a['user']['id']}", headers=ha).status_code == 400


def test_super_admin_lists_and_suspends_tenants(client, make_super_admin):
    a, b, ha, hb = two_tenants(client)
    make_super_admin()
    hs = auth_headers(client, "root@supportpilot.io")

    assert len(client.get(f"{API}/admin/tenants", headers=hs).json()) == 2

    r = client.patch(f"{API}/admin/tenants/{a['tenant']['id']}/status", headers=hs, json={"status": "suspended"})
    assert r.status_code == 200 and r.json()["status"] == "suspended"

    # Tenant A is locked out immediately, even with a token issued before suspension
    assert client.get(f"{API}/users", headers=ha).status_code == 403
    login = client.post(f"{API}/auth/login", data={"username": "admin@acme.com", "password": "Passw0rd123"})
    assert login.status_code == 403
    # Tenant B unaffected
    assert client.get(f"{API}/users", headers=hb).status_code == 200

    client.patch(f"{API}/admin/tenants/{a['tenant']['id']}/status", headers=hs, json={"status": "active"})
    assert client.get(f"{API}/users", headers=ha).status_code == 200