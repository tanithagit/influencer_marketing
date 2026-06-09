import pytest


def test_apply_to_campaign(client, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "I want to apply!",
        "proposed_rate":    500
    }, headers=influencer_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["status"]     == "pending"
    assert data["campaign_id"] == campaign_id


def test_duplicate_application(client, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "First application"
    }, headers=influencer_headers)

    res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Second application"
    }, headers=influencer_headers)
    assert res.status_code == 400
    assert "already applied" in res.json()["detail"]


def test_brand_cannot_apply(client, brand_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Brand trying to apply"
    }, headers=brand_headers)
    assert res.status_code == 403


def test_approve_application(client, brand_headers, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]

    # Apply
    app_res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Apply"
    }, headers=influencer_headers)
    app_id = app_res.json()["id"]

    # Approve
    res = client.put(
        f"/api/applications/{app_id}/approve",
        headers=brand_headers
    )
    assert res.status_code == 200
    assert res.json()["status"] == "approved"


def test_reject_application(client, brand_headers, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]

    app_res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Apply"
    }, headers=influencer_headers)
    app_id = app_res.json()["id"]

    res = client.put(
        f"/api/applications/{app_id}/reject",
        headers=brand_headers
    )
    assert res.status_code == 200
    assert res.json()["status"] == "rejected"


def test_cannot_approve_twice(client, brand_headers, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]

    app_res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Apply"
    }, headers=influencer_headers)
    app_id = app_res.json()["id"]

    client.put(f"/api/applications/{app_id}/approve", headers=brand_headers)

    res = client.put(
        f"/api/applications/{app_id}/approve",
        headers=brand_headers
    )
    assert res.status_code == 400


def test_get_my_applications(client, influencer_headers, sample_campaign):
    campaign_id = sample_campaign["id"]
    client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Apply"
    }, headers=influencer_headers)

    res = client.get("/api/applications/my-applications", headers=influencer_headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1