"""Social & Marketplace Deep Harvester (AGENT 27).
Extracts structured sofa specifications from Facebook, Instagram, TikTok, and Ouedkniss post text.
Copyright (c) 2026 saifiwalid.
"""

import re
from app.security import neutralize_untrusted_content
from app.services.geo_algeria import resolve_wilaya_from_text
from app.services.multilingual_search import normalize_algerian_price_to_dzd


def detect_social_platform(url: str) -> str:
    lowered = url.lower()
    if "facebook.com" in lowered or "fb.com" in lowered or "fb.watch" in lowered:
        return "facebook_marketplace" if "marketplace" in lowered else "facebook_page"
    if "instagram.com" in lowered:
        return "instagram_business"
    if "tiktok.com" in lowered:
        return "tiktok_shop"
    if "ouedkniss.com" in lowered:
        return "ouedkniss"
    return "web_listing"


def extract_social_listing_metadata(raw_text: str, source_url: str = "") -> dict:
    """Parse unstructured social post text (AR / Darja / FR) into structured sofa fields."""
    safe_text = neutralize_untrusted_content(raw_text)
    lowered = safe_text.lower()

    price_dzd, price_status = normalize_algerian_price_to_dzd(safe_text)
    wilaya = resolve_wilaya_from_text(safe_text)

    foam_match = re.search(r"\b(d\s*20|d\s*25|d\s*28|d\s*30|d\s*32|d\s*35|d\s*36|d\s*40|d\s*45|d\s*50|hr)\b", lowered)
    foam_density = re.sub(r"\s+", "", foam_match.group(1)).upper() if foam_match else None

    wood_type = None
    if any(k in lowered for k in ("زان", "hêtre", "hetre")):
        wood_type = "Hêtre"
    elif any(k in lowered for k in ("بلوط", "chêne", "chene")):
        wood_type = "Chêne"
    elif any(k in lowered for k in ("صنوبر", "pin")):
        wood_type = "Pin"
    elif "mdf" in lowered:
        wood_type = "MDF"

    fabric_type = None
    if any(k in lowered for k in ("anti-tache", "anti tache", "بقع", "يتوسخ")):
        fabric_type = "Tissu anti-tache"
    elif any(k in lowered for k in ("velours", "قطيفة")):
        fabric_type = "Velours"
    elif any(k in lowered for k in ("chenille", "شينيل")):
        fabric_type = "Chenille"
    elif any(k in lowered for k in ("bouclé", "boucle", "بوكلي")):
        fabric_type = "Bouclé"

    sofa_type = "l_shape" if any(k in lowered for k in ("angle", "زاوية", "en l", "ل")) else (
        "u_shape" if "en u" in lowered or "صالون u" in lowered else (
            "turkish" if any(k in lowered for k in ("turc", "تركي")) else "modern"
        )
    )

    return {
        "platform": detect_social_platform(source_url) if source_url else "facebook_page",
        "extracted_price_dzd": price_dzd,
        "price_status": price_status,
        "wilaya": wilaya,
        "foam_density_claimed": foam_density,
        "wood_type": wood_type,
        "fabric_type": fabric_type,
        "sofa_type": sofa_type,
        "sanitized_text": safe_text,
    }
