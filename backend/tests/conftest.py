import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.models import (
    User, Campaign, CampaignApplication,
    Deliverable, Payment, Subscription
)

# Use separate test database
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def brand_token(client):
    client.post("/api/auth/register", json={
        "email":     "brand@test.com",
        "password":  "password123",
        "full_name": "Test Brand",
        "role":      "brand"
    })
    res = client.post("/api/auth/login", json={
        "email":    "brand@test.com",
        "password": "password123"
    })
    return res.json()["access_token"]


@pytest.fixture
def influencer_token(client):
    client.post("/api/auth/register", json={
        "email":     "influencer@test.com",
        "password":  "password123",
        "full_name": "Test Influencer",
        "role":      "influencer"
    })
    res = client.post("/api/auth/login", json={
        "email":    "influencer@test.com",
        "password": "password123"
    })
    return res.json()["access_token"]


@pytest.fixture
def brand_headers(brand_token):
    return {"Authorization": f"Bearer {brand_token}"}


@pytest.fixture
def influencer_headers(influencer_token):
    return {"Authorization": f"Bearer {influencer_token}"}


@pytest.fixture
def sample_campaign(client, brand_headers):
    res = client.post("/api/campaigns/", json={
        "title":       "Test Campaign",
        "description": "Test Description",
        "budget":      1000.0,
        "niche":       "Technology",
        "start_date":  "2026-07-01T00:00:00",
        "end_date":    "2026-12-01T00:00:00"
    }, headers=brand_headers)
    return res.json()