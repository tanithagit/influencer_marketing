import pytest
import io


def create_approved_application(client, brand_headers, influencer_headers):
    campaign_res = client.post("/api/campaigns/", json={
        "title":      "Payment Test Campaign",
        "budget":     1000.0,
        "start_date": "2026-07-01T00:00:00",
        "end_date":   "2026-12-01T00:00:00"
    }, headers=brand_headers)
    campaign_id = campaign_res.json()["id"]

    app_res = client.post(f"/api/applications/campaign/{campaign_id}", json={
        "proposal_message": "Apply",
        "proposed_rate":    500
    }, headers=influencer_headers)
    app_id = app_res.json()["id"]

    influencer_id = app_res.json()["influencer_id"]

    client.put(
        f"/api/applications/{app_id}/approve",
        headers=brand_headers
    )

    return campaign_id, app_id, influencer_id


def test_payment_blocked_without_deliverable(
    client, brand_headers, influencer_headers
):
    campaign_id, _, influencer_id = create_approved_application(
        client, brand_headers, influencer_headers
    )

    # Try payment without deliverable
    pay_res = client.post("/api/payments/create-intent", json={
        "campaign_id":   campaign_id,
        "influencer_id": influencer_id,
        "amount":        500.0
    }, headers=brand_headers)

    # Payment intent can be created
    # But release should fail without approved deliverable
    if pay_res.status_code == 201:
        payment_id = pay_res.json()["payment_id"]
        release_res = client.put(
            f"/api/payments/{payment_id}/release",
            headers=brand_headers
        )
        assert release_res.status_code == 400
        assert "deliverable" in release_res.json()["detail"].lower()


def test_influencer_cannot_create_payment(
    client, influencer_headers
):
    res = client.post("/api/payments/create-intent", json={
        "campaign_id":   1,
        "influencer_id": 1,
        "amount":        100.0
    }, headers=influencer_headers)
    assert res.status_code == 403


def test_get_my_earnings(client, influencer_headers):
    res = client.get("/api/payments/my-earnings", headers=influencer_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)