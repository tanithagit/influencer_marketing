import pytest


def test_register_brand(client):
    res = client.post("/api/auth/register", json={
        "email":     "newbrand@test.com",
        "password":  "password123",
        "full_name": "New Brand",
        "role":      "brand"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "newbrand@test.com"
    assert data["role"]  == "brand"
    assert "hashed_password" not in data


def test_register_influencer(client):
    res = client.post("/api/auth/register", json={
        "email":     "newinfluencer@test.com",
        "password":  "password123",
        "full_name": "New Influencer",
        "role":      "influencer"
    })
    assert res.status_code == 201
    assert res.json()["role"] == "influencer"


def test_register_duplicate_email(client):
    client.post("/api/auth/register", json={
        "email":     "duplicate@test.com",
        "password":  "password123",
        "full_name": "User One",
        "role":      "brand"
    })
    res = client.post("/api/auth/register", json={
        "email":     "duplicate@test.com",
        "password":  "password123",
        "full_name": "User Two",
        "role":      "brand"
    })
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]


def test_login_success(client):
    client.post("/api/auth/register", json={
        "email":     "logintest@test.com",
        "password":  "password123",
        "full_name": "Login Test",
        "role":      "brand"
    })
    res = client.post("/api/auth/login", json={
        "email":    "logintest@test.com",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email":     "wrongpass@test.com",
        "password":  "password123",
        "full_name": "Wrong Pass",
        "role":      "brand"
    })
    res = client.post("/api/auth/login", json={
        "email":    "wrongpass@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401


def test_get_me(client, brand_headers):
    res = client.get("/api/auth/me", headers=brand_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "brand@test.com"


# ✅ New - correct status code
def test_get_me_without_token(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 403 or res.status_code == 401