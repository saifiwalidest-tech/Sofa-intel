"""Web Reach Service — Unified Live Internet Search & Public URL Reader for SOFA INTEL DZ.
Inspired by Agent Reach (MIT) unified channel architecture with SSRF & Prompt-Injection guards.
Copyright (c) 2026 saifiwalid.
"""

import html as html_lib
import re
from urllib.parse import quote_plus, unquote

import httpx

from app.agents.social_harvester import detect_social_platform, extract_social_listing_metadata
from app.config import get_settings
from app.security import neutralize_untrusted_content, validate_external_url
from app.services.geo_algeria import WILAYA_BY_CODE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "ar,fr;q=0.9,en;q=0.8",
}


def _clean_html_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def search_live_web(query: str, wilaya_code: str | None = None, platform: str | None = None, limit: int = 8) -> dict:
    """Search public web & indexed social/marketplace listings via DuckDuckGo HTML (no API key required)."""
    safe_q = neutralize_untrusted_content(query).strip()
    if not safe_q:
        return {"ok": False, "channel": "web", "action": "search", "items": [], "error": {"code": "BAD_INPUT", "message": "Empty query"}}

    terms = [safe_q, "salon", "الجزائر"]
    if wilaya_code and wilaya_code in WILAYA_BY_CODE:
        w = WILAYA_BY_CODE[wilaya_code]
        terms.append(w["name_fr"])

    if platform == "facebook_marketplace" or platform == "facebook_page":
        terms.append("site:facebook.com")
    elif platform == "instagram":
        terms.append("site:instagram.com")
    elif platform == "tiktok":
        terms.append("site:tiktok.com")
    elif platform == "ouedkniss":
        terms.append("site:ouedkniss.com")

    full_query = " ".join(terms)
    settings = get_settings()

    # Optional official Google CSE if configured
    if settings.google_cse_api_key and settings.google_cse_cx:
        try:
            with httpx.Client(timeout=10.0) as client:
                r = client.get(
                    "https://www.googleapis.com/customsearch/v1",
                    params={"key": settings.google_cse_api_key, "cx": settings.google_cse_cx, "q": full_query, "num": min(limit, 10)},
                )
                if r.status_code == 200:
                    data = r.json()
                    items = []
                    for it in data.get("items", []):
                        url = it.get("link", "")
                        items.append({
                            "title": neutralize_untrusted_content(it.get("title", "")),
                            "snippet": neutralize_untrusted_content(it.get("snippet", "")),
                            "url": url,
                            "platform": detect_social_platform(url),
                            "source": "google_cse",
                        })
                    return {"ok": True, "channel": "web", "action": "search", "query": full_query, "items": items, "error": None}
        except Exception:
            pass

    # Fallback: Public DuckDuckGo HTML Search
    try:
        ddg_url = f"https://html.duckduckgo.com/html/?q={quote_plus(full_query)}"
        with httpx.Client(timeout=12.0, follow_redirects=True, headers=HEADERS) as client:
            resp = client.get(ddg_url)
            if resp.status_code != 200:
                return {
                    "ok": False,
                    "channel": "web",
                    "action": "search",
                    "query": full_query,
                    "items": [],
                    "error": {"code": "RATE_LIMITED", "message": f"Upstream status {resp.status_code}"},
                }

        pattern = re.compile(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?'
            r'(?:<a[^>]*class="result__snippet"[^>]*>(.*?)</a>|<div[^>]*class="result__snippet"[^>]*>(.*?)</div>)',
            re.S | re.I,
        )
        items = []
        for match in pattern.finditer(resp.text):
            raw_href = match.group(1)
            # Extract real URL from DDG uddg redirect if present
            m_uddg = re.search(r"uddg=([^&]+)", raw_href)
            real_url = unquote(m_uddg.group(1)) if m_uddg else raw_href
            if not real_url.startswith(("http://", "https://")):
                continue
            title = neutralize_untrusted_content(_clean_html_text(match.group(2)))
            snippet_raw = match.group(3) or match.group(4) or ""
            snippet = neutralize_untrusted_content(_clean_html_text(snippet_raw))
            parsed_specs = extract_social_listing_metadata(f"{title} {snippet}", real_url)
            items.append({
                "title": title,
                "snippet": snippet,
                "url": real_url,
                "platform": detect_social_platform(real_url),
                "extracted_price_dzd": parsed_specs.get("extracted_price_dzd"),
                "foam_density_claimed": parsed_specs.get("foam_density_claimed"),
                "wood_type": parsed_specs.get("wood_type"),
                "source": "live_web_index",
            })
            if len(items) >= limit:
                break

        return {"ok": True, "channel": "web", "action": "search", "query": full_query, "items": items, "error": None}
    except httpx.TimeoutException:
        return {"ok": False, "channel": "web", "action": "search", "query": full_query, "items": [], "error": {"code": "TIMEOUT", "message": "Live web search timed out"}}
    except Exception as exc:
        return {"ok": False, "channel": "web", "action": "search", "query": full_query, "items": [], "error": {"code": "UPSTREAM_BROKEN", "message": str(exc)[:160]}}


def read_public_url(url: str) -> dict:
    """Fetch a public web/listing URL cleanly via Jina Reader / direct HTTP and extract sofa specs."""
    safe_url = validate_external_url(url)
    reader_url = f"https://r.jina.ai/{safe_url}"
    content = ""
    backend_used = "jina_reader"

    try:
        with httpx.Client(timeout=12.0, follow_redirects=True, headers=HEADERS) as client:
            r = client.get(reader_url)
            if r.status_code == 200 and len(r.text.strip()) > 40:
                content = r.text[:6000]
            else:
                backend_used = "direct_http"
                r2 = client.get(safe_url)
                if r2.status_code == 200:
                    content = _clean_html_text(r2.text)[:6000]
                else:
                    return {
                        "ok": False,
                        "channel": detect_social_platform(safe_url),
                        "action": "read",
                        "url": safe_url,
                        "error": {"code": "UPSTREAM_BROKEN", "message": f"HTTP {r2.status_code}"},
                    }
    except Exception as exc:
        return {
            "ok": False,
            "channel": detect_social_platform(safe_url),
            "action": "read",
            "url": safe_url,
            "error": {"code": "TIMEOUT", "message": str(exc)[:160]},
        }

    extracted = extract_social_listing_metadata(content, safe_url)
    return {
        "ok": True,
        "channel": extracted["platform"],
        "action": "read",
        "backend": backend_used,
        "url": safe_url,
        "extracted": extracted,
        "error": None,
    }


def run_channel_doctor() -> dict:
    """Diagnostic status for all internet & social discovery channels."""
    settings = get_settings()
    return {
        "channels": [
            {"id": "web_live_search", "name": "البحث المباشر عبر الإنترنت (DuckDuckGo / Google CSE)", "status": "ok", "requires_key": False},
            {"id": "url_reader", "name": "قارئ الروابط العامة واستخراج المواصفات (Jina / HTTP)", "status": "ok", "requires_key": False},
            {"id": "facebook_public", "name": "منشورات وصفحات فيسبوك المفهرسة", "status": "ok" if settings.facebook_graph_access_token else "indexed_fallback", "requires_key": True},
            {"id": "instagram_public", "name": "عروض إنستغرام المفهرسة", "status": "ok" if settings.instagram_graph_access_token else "indexed_fallback", "requires_key": True},
            {"id": "tiktok_public", "name": "مقاطع وعروض تيك توك المفهرسة", "status": "ok" if settings.tiktok_research_api_key else "indexed_fallback", "requires_key": True},
            {"id": "ouedkniss_public", "name": "فهرس إعلانات Ouedkniss", "status": "ok", "requires_key": False},
        ]
    }
