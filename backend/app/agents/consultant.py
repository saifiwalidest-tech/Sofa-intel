"""AGENT 17 — AI Shopping Consultant (AR / Darja / Latin-Darja / FR / EN).
Parses natural language requests into structured filters and explains evidence-based picks.
Copyright (c) 2026 saifiwalid.
"""

import re
from app.services.geo_algeria import resolve_wilaya_from_text, estimate_delivery_dzd
from app.services.multilingual_search import normalize_algerian_price_to_dzd
from app.security import neutralize_untrusted_content


def parse_consultant_intent(raw_message: str, fallback_wilaya: str | None = None) -> dict:
    safe_msg = neutralize_untrusted_content(raw_message)
    lowered = safe_msg.lower()

    # Budget extraction (supports DZD and Algerian centimes)
    budget_dzd, price_status = normalize_algerian_price_to_dzd(safe_msg)

    # Sofa type
    sofa_type = None
    if any(k in lowered for k in ("l", "زاوية", "angle", "كوان", "coin")):
        sofa_type = "l_shape"
    elif any(k in lowered for k in ("u", "صالون u")):
        sofa_type = "u_shape"
    elif any(k in lowered for k in ("سرير", "clic", "convertible", "lit")):
        sofa_type = "sofa_bed"
    elif any(k in lowered for k in ("تركي", "turc", "turkish")):
        sofa_type = "turkish"
    elif any(k in lowered for k in ("مغربي", "marocain", "sdader")):
        sofa_type = "moroccan"

    # Foam density
    foam_density = None
    m_foam = re.search(r"(d\s*36|36|d\s*40|40|d\s*35|35|hr|d\s*45)", lowered)
    if m_foam:
        token = re.sub(r"\s+", "", m_foam.group(1)).upper()
        foam_density = token if token.startswith(("D", "HR")) else f"D{token}"

    # Wood type
    wood_type = None
    if any(k in lowered for k in ("زان", "hêtre", "hetre", "beech")):
        wood_type = "Hêtre"
    elif any(k in lowered for k in ("بلوط", "chêne", "chene")):
        wood_type = "Chêne"
    elif any(k in lowered for k in ("صنوبر", "pin")):
        wood_type = "Pin"

    # Stain resistant / easy clean
    stain_resistant = any(
        k in lowered for k in ("يتوسخ", "بقع", "anti-tache", "anti tache", "déperlant", "تنظيف", "stain")
    )

    # Wilaya
    wilaya_obj = resolve_wilaya_from_text(safe_msg)
    wilaya_code = wilaya_obj["code"] if wilaya_obj else fallback_wilaya

    return {
        "sanitized_query": safe_msg,
        "budget_dzd": budget_dzd,
        "price_parse_status": price_status,
        "sofa_type": sofa_type,
        "foam_density": foam_density,
        "wood_type": wood_type,
        "stain_resistant": stain_resistant,
        "wilaya_code": wilaya_code,
        "wilaya_name": wilaya_obj["name_ar"] if wilaya_obj else None,
    }


def build_consultant_response(intent: dict, candidates: list[dict]) -> dict:
    user_wilaya = intent.get("wilaya_code") or "16"
    ranked: list[dict] = []

    for p in candidates:
        seller_w = p["seller"]["wilaya_code"]
        est_deliv, dist_km = estimate_delivery_dzd(seller_w, user_wilaya)
        delivered_total = p["current_price_dzd"] + (p["delivery_cost_dzd"] if p.get("delivery_cost_dzd") is not None else est_deliv)

        score = p["quality_score_midpoint"] * 0.5 + p["value_for_money_score"] * 0.35 + p["evidence_confidence_score"] * 0.15
        if intent.get("budget_dzd") and delivered_total <= intent["budget_dzd"]:
            score += 15.0
        if intent.get("sofa_type") and p["sofa_type"] == intent["sofa_type"]:
            score += 12.0
        if intent.get("foam_density") and (p.get("foam_density_claimed") or "").upper() == intent["foam_density"]:
            score += 12.0
        if intent.get("wood_type") and intent["wood_type"].lower() in (p.get("wood_type") or "").lower():
            score += 10.0
        if intent.get("stain_resistant") and any("anti" in prop.lower() or "déperlant" in prop.lower() or "بقع" in prop for prop in p.get("fabric_properties", [])):
            score += 10.0
        if seller_w == user_wilaya:
            score += 8.0

        ranked.append({
            "product": p,
            "match_score": round(score, 1),
            "estimated_delivery_to_user_dzd": est_deliv,
            "distance_km": dist_km,
            "estimated_delivered_total_dzd": delivered_total,
        })

    ranked.sort(key=lambda x: -x["match_score"])
    top_picks = ranked[:3]

    parts = []
    if intent.get("budget_dzd"):
        parts.append(f"الميزانية المستخرجة: {intent['budget_dzd']:,} دج")
    if intent.get("sofa_type"):
        parts.append(f"الشكل: {intent['sofa_type']}")
    if intent.get("foam_density"):
        parts.append(f"الرغوة المطلوبة: {intent['foam_density']}")
    if intent.get("wood_type"):
        parts.append(f"الخشب المطلوب: {intent['wood_type']}")
    if intent.get("wilaya_name"):
        parts.append(f"الولاية: {intent['wilaya_name']}")

    summary = "تم تحليل طلبك ومطابقته مع المواصفات الهندسية وأسعار السوق والتوصيل: " + (" | ".join(parts) if parts else "")
    if not top_picks:
        summary += " لم يتم العثور على عروض مطابقة تماماً حالياً."
    else:
        best = top_picks[0]["product"]
        summary += (
            f" أفضل ترشيح حالياً هو «{best['title']}» بسعر {best['current_price_dzd']:,} دج "
            f"(نطاق الجودة: {best['quality_score_min']}–{best['quality_score_max']}/100، "
            f"اكتمال البيانات: {best['data_completeness_score']}%)."
        )

    return {
        "agent": "AGENT_17",
        "understood_criteria": intent,
        "summary_ar": summary,
        "recommendations": top_picks,
    }
