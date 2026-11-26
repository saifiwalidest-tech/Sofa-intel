"""Source Adapters Layer — Authorized Data Collection & Provenance Tracking.
Copyright (c) 2026 saifiwalid.
"""

from datetime import datetime, timezone
from dataclasses import dataclass
from app.config import get_settings


@dataclass
class SourceAdapterInfo:
    id: str
    name: str
    access_method: str
    status: str  # connected | limited | requires_auth | unavailable
    usage_rules: str
    available_fields: list[str]
    rate_limit_rpm: int
    cache_ttl_seconds: int
    last_successful_sync: str | None
    notes: str


def get_all_adapter_statuses() -> list[dict]:
    settings = get_settings()
    now_iso = datetime.now(timezone.utc).isoformat()

    adapters = [
        SourceAdapterInfo(
            id="manual_verified",
            name="User-Submitted & Partner Catalog",
            access_method="Direct REST Form / Partner Feed",
            status="connected",
            usage_rules="Requires valid public URL and seller verification",
            available_fields=["title", "price", "wilaya", "foam", "wood", "fabric", "warranty"],
            rate_limit_rpm=60,
            cache_ttl_seconds=300,
            last_successful_sync=now_iso,
            notes="Active and ready for direct user/factory submissions.",
        ),
        SourceAdapterInfo(
            id="public_web_index",
            name="Global Web Discovery (Google/Bing CSE)",
            access_method="Official Custom Search JSON API",
            status="connected" if settings.google_cse_api_key else "requires_auth",
            usage_rules="Respects robots.txt & API daily quota",
            available_fields=["title", "snippet", "source_url", "published_at"],
            rate_limit_rpm=30,
            cache_ttl_seconds=3600,
            last_successful_sync=now_iso if settings.google_cse_api_key else None,
            notes="Set GOOGLE_CSE_API_KEY & GOOGLE_CSE_CX in .env to enable live CSE queries.",
        ),
        SourceAdapterInfo(
            id="ouedkniss_adapter",
            name="Ouedkniss Public Listings",
            access_method="User-Submitted URLs & Authorized Partner Feed",
            status="limited",
            usage_rules="No automated scraping bypassing anti-bot or login walls",
            available_fields=["title", "price", "wilaya", "commune", "description", "source_url"],
            rate_limit_rpm=15,
            cache_ttl_seconds=1800,
            last_successful_sync=now_iso,
            notes="Accepts user-provided Ouedkniss listing links with SSRF & XSS sanitization.",
        ),
        SourceAdapterInfo(
            id="facebook_adapter",
            name="Facebook Public Pages & Marketplace",
            access_method="Meta Graph API (Authorized Token)",
            status="connected" if settings.facebook_graph_access_token else "requires_auth",
            usage_rules="Strictly authorized public commercial pages; no login bypass",
            available_fields=["page_name", "post_text", "images", "location"],
            rate_limit_rpm=20,
            cache_ttl_seconds=3600,
            last_successful_sync=now_iso if settings.facebook_graph_access_token else None,
            notes="Requires FACEBOOK_GRAPH_ACCESS_TOKEN.",
        ),
        SourceAdapterInfo(
            id="instagram_adapter",
            name="Instagram Business Profiles",
            access_method="Instagram Graph API",
            status="connected" if settings.instagram_graph_access_token else "requires_auth",
            usage_rules="Official Business Discovery API only",
            available_fields=["caption", "media_url", "timestamp", "username"],
            rate_limit_rpm=20,
            cache_ttl_seconds=3600,
            last_successful_sync=now_iso if settings.instagram_graph_access_token else None,
            notes="Requires INSTAGRAM_GRAPH_ACCESS_TOKEN.",
        ),
        SourceAdapterInfo(
            id="tiktok_adapter",
            name="TikTok Furniture Makers",
            access_method="TikTok Research / Display API",
            status="connected" if settings.tiktok_research_api_key else "requires_auth",
            usage_rules="Authorized API & manual video metadata/transcript input",
            available_fields=["video_desc", "transcript", "ocr_text", "creator"],
            rate_limit_rpm=15,
            cache_ttl_seconds=3600,
            last_successful_sync=now_iso if settings.tiktok_research_api_key else None,
            notes="Requires TIKTOK_RESEARCH_API_KEY.",
        ),
        SourceAdapterInfo(
            id="demo_seed",
            name="Synthetic Demo Dataset (Testing Only)",
            access_method="Local Seeded Database (is_demo=true)",
            status="connected",
            usage_rules="Strictly labeled as DEMO DATA; never presented as live scraped offers",
            available_fields=["all_fields"],
            rate_limit_rpm=1000,
            cache_ttl_seconds=60,
            last_successful_sync=now_iso,
            notes="Provides realistic Algerian market test scenarios for Blida, Alger, Sétif, Oran, Constantine, Tizi Ouzou.",
        ),
    ]
    return [a.__dict__ for a in adapters]
