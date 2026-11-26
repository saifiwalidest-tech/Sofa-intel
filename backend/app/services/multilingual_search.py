"""Multilingual Search Engine & Algerian Price Normalizer (AR / Darja / Latin-Darja / FR / EN).
Copyright (c) 2026 saifiwalid.
"""

import re

SYNONYM_GROUPS: list[set[str]] = [
    {"كنبة", "أريكة", "صالون", "فوتاي", "canapé", "canape", "salon", "fauteuil", "sofa", "couch"},
    {"زاوية", "l", "l_shape", "angle", "en l", "canapé d'angle", "صالون زاوية", "كوان", "coin"},
    {"تركي", "turkish", "turc", "تركية", "صالون تركي"},
    {"مغربي", "moroccan", "marocain", "سدادر", "sdader"},
    {"رغوة", "إسفنج", "موس", "mousse", "foam", "ponja", "بونج"},
    {"d36", "موس 36", "mousse 36", "36", "كثافة 36"},
    {"d35", "موس 35", "mousse 35"},
    {"d40", "موس 40", "mousse 40"},
    {"hr", "high resilience", "haute résilience", "مرنة"},
    {"زان", "خشب الزان", "hêtre", "hetre", "beech", "bois hetres", "hétre"},
    {"بلوط", "chêne", "chene", "oak"},
    {"صنوبر", "pin", "pine", "خشب أحمر", "bois rouge"},
    {"مقاوم للبقع", "anti-tache", "anti tache", "déperlant", "deperlant", "ما يتوسخش", "stain resistant"},
    {"قطيفة", "velours", "velvet"},
    {"شينيل", "chenille"},
    {"ميكروفيبر", "microfibre", "microfiber"},
]


def expand_multilingual_query(query: str) -> list[str]:
    """Expand a user query into normalized search tokens & Algerian synonyms."""
    q = query.strip().lower()
    if not q:
        return []
    tokens = [t for t in re.split(r"[\s,،;+\-/]+", q) if len(t) >= 1]
    expanded: set[str] = set(tokens)
    for group in SYNONYM_GROUPS:
        for term in group:
            if term in q or any(t == term for t in tokens):
                expanded.update(group)
                break
    return sorted(expanded)


def normalize_algerian_price_to_dzd(text: str) -> tuple[int | None, str]:
    """Distinguish DZD vs Algerian Centimes ('مليون سنتيم').
    Returns (price_dzd, status).
    """
    lowered = text.lower().replace(",", ".")
    # e.g., "12 مليون" or "12 millions" -> 12 * 10,000 DZD = 120,000 DZD
    m_million = re.search(r"(\d+(?:\.\d+)?)\s*(مليون|ملاين|ملايين|million|millions|mlyoun)", lowered)
    if m_million:
        val = float(m_million.group(1))
        return int(round(val * 10000)), "normalized_from_centimes"

    # e.g., "120000 da" or "120 000 dzd" or "120000 دج"
    m_dzd = re.search(r"(\d[\d\s]{3,8})\s*(da|dzd|دج|دينار)", lowered)
    if m_dzd:
        digits = int(re.sub(r"\s+", "", m_dzd.group(1)))
        return digits, "confirmed_dzd"

    return None, "ambiguous_price"
