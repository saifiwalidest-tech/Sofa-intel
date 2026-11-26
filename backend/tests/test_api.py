"""API Integration tests for SOFA INTEL DZ FastAPI backend.
Copyright (c) 2026 saifiwalid.
"""

from fastapi.testclient import TestClient
from app.main import app


def test_health_and_core_endpoints():
    with TestClient(app) as client:
        r_health = client.get("/health")
        assert r_health.status_code == 200
        assert r_health.json()["copyright"] == "saifiwalid"

        r_prod = client.get("/api/v1/products")
        assert r_prod.status_code == 200
        items = r_prod.json()["items"]
        assert len(items) >= 6
        assert all(it["is_demo"] is True for it in items)

        r_compare = client.post("/api/v1/compare", json={"product_ids": ["demo-sofa-001", "demo-sofa-002"]})
        assert r_compare.status_code == 200
        assert "insights" in r_compare.json()

        r_consult = client.post(
            "/api/v1/consultant/ask",
            json={"message": "عندي ميزانية 12 مليون سنتيم صالون L D36 زان البليدة"},
        )
        assert r_consult.status_code == 200
        assert len(r_consult.json()["recommendations"]) > 0

        r_adapters = client.get("/api/v1/adapters/status")
        assert r_adapters.status_code == 200
        assert len(r_adapters.json()["adapters"]) >= 6

        r_agents = client.get("/api/v1/agents/status")
        assert r_agents.status_code == 200
        assert r_agents.json()["total_agents"] == 28

        r_mfg = client.get("/api/v1/manufacturers")
        assert r_mfg.status_code == 200
        wilaya_codes = {s["wilaya_code"] for s in r_mfg.json()["items"]}
        assert len(wilaya_codes) == 58

        r_social = client.post(
            "/api/v1/social/extract",
            json={
                "text": "صالون زاوية L في وهران رغوة D36 خشب الزان بـ 12 مليون سنتيم قماش anti-tache",
                "source_url": "https://www.facebook.com/marketplace/item/123",
            },
        )
        assert r_social.status_code == 200
        assert r_social.json()["platform"] == "facebook_marketplace"
        assert r_social.json()["extracted_price_dzd"] == 120000
