import pytest


def test_create_campaign(client, brand_headers):
    res = client.post("/api/campaigns/", json={
        "title":       "My Campaign",
        "description": "Description",
        "budget":      5000.0,
        "niche":       "Technology",
        "start_date":  "2026-07-01T00:00:00",
        "end_date":    "2026-12-01T00:00:00"
    }, headers=brand_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["title"]  == "My Campaign"
    assert data["budget"] == 5000.0
    assert data["status"] == "active"


def test_influencer_cannot_create_campaign(client, influencer_headers):
    res = client.post("/api/campaigns/", json={
        "title":      "Hacked Campaign",
        "budget":     100.0,
        "start_date": "2026-07-01T00:00:00",
        "end_date":   "2026-12-01T00:00:00"
    }, headers=influencer_headers)
    assert res.status_code == 403


def test_create_campaign_invalid_dates(client, brand_headers):
    res = client.post("/api/campaigns/", json={
        "title":      "Bad Dates",
        "budget":     100.0,
        "start_date": "2026-12-01T00:00:00",
        "end_date":   "2026-07-01T00:00:00"
    }, headers=brand_headers)
    assert res.status_code == 400


def test_list_campaigns(client, brand_headers, sample_campaign):
    res = client.get("/api/campaigns/", headers=brand_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_campaign_by_id(client, brand_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    res = client.get(f"/api/campaigns/{campaign_id}", headers=brand_headers)
    assert res.status_code == 200
    assert res.json()["id"] == campaign_id


def test_brand_campaign_limit_free_plan(client, brand_headers):
    for i in range(3):
        client.post("/api/campaigns/", json={
            "title":      f"Campaign {i}",
            "budget":     100.0,
            "start_date": "2026-07-01T00:00:00",
            "end_date":   "2026-12-01T00:00:00"
        }, headers=brand_headers)

    # 4th campaign should fail
    res = client.post("/api/campaigns/", json={
        "title":      "Campaign 4",
        "budget":     100.0,
        "start_date": "2026-07-01T00:00:00",
        "end_date":   "2026-12-01T00:00:00"
    }, headers=brand_headers)
    assert res.status_code == 403
    assert "Free plan" in res.json()["detail"]


def test_update_campaign(client, brand_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    res = client.put(f"/api/campaigns/{campaign_id}", json={
        "title": "Updated Title"
    }, headers=brand_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Title"


def test_delete_campaign(client, brand_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    res = client.delete(
        f"/api/campaigns/{campaign_id}",
        headers=brand_headers
    )
    assert res.status_code == 200