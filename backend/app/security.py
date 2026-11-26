"""Security utilities: XSS/Prompt Injection sanitization, SSRF guard, Rate Limiter, RBAC.
Copyright (c) 2026 saifiwalid.
"""

import html
import ipaddress
import re
import time
from collections import defaultdict, deque
from urllib.parse import urlparse

from fastapi import HTTPException, Request, status

PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions", re.I),
    re.compile(r"(reveal|print|show)\s+(your\s+)?(system\s+prompt|api[_\s]?key|secret)", re.I),
    re.compile(r"<\s*/?\s*system\s*>", re.I),
    re.compile(r"you\s+are\s+now\s+(a\s+)?(dan|developer\s+mode)", re.I),
    re.compile(r"execute\s+(shell|bash|cmd|sql)", re.I),
]

SCRIPT_TAG_PATTERN = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.I | re.S)


def sanitize_text(value: str | None, max_len: int = 4000) -> str:
    """Escape HTML/XSS vectors and strip script tags from untrusted external text."""
    if not value:
        return ""
    cleaned = SCRIPT_TAG_PATTERN.sub("", value.strip())
    cleaned = html.escape(cleaned, quote=True)
    return cleaned[:max_len]


def detect_prompt_injection(text: str | None) -> tuple[bool, list[str]]:
    """Detect prompt injection attempts in untrusted external listing text or queries."""
    if not text:
        return False, []
    matched = [p.pattern for p in PROMPT_INJECTION_PATTERNS if p.search(text)]
    return len(matched) > 0, matched


def neutralize_untrusted_content(text: str | None) -> str:
    """Wrap and sanitize external content so agents treat it strictly as data."""
    cleaned = sanitize_text(text)
    flagged, _ = detect_prompt_injection(cleaned)
    if flagged:
        return "[UNTRUSTED_CONTENT_FILTERED: potential instruction-like pattern neutralized]"
    return cleaned


def validate_external_url(url: str) -> str:
    """SSRF Guard: only allow public http/https URLs; block localhost and private CIDRs."""
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL scheme or missing hostname.",
        )

    host = parsed.hostname.lower()
    if host in ("localhost", "127.0.0.1", "::1", "0.0.0.0", "metadata.google.internal"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SSRF Guard: internal hostnames are blocked.",
        )

    try:
        ip_obj = ipaddress.ip_address(host)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SSRF Guard: private or reserved IP addresses are blocked.",
            )
    except ValueError:
        pass  # Hostname is a domain name, not an IP literal.

    return url.strip()


class InMemoryRateLimiter:
    """Sliding-window rate limiter per client IP."""

    def __init__(self, max_requests_per_minute: int = 120):
        self.max_requests = max_requests_per_minute
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = self._hits[client_ip]
        while window and now - window[0] > 60.0:
            window.popleft()
        if len(window) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please retry in a minute.",
            )
        window.append(now)


def require_role(request: Request, allowed_roles: tuple[str, ...]) -> str:
    """Lightweight RBAC check via X-User-Role header (defaults to consumer)."""
    role = request.headers.get("X-User-Role", "consumer").lower()
    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role}' is not authorized for this operation.",
        )
    return role
