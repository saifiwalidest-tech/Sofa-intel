"""Verification, Pricing, Trust & Vision Constraints Agents (AGENT 11, 12, 14, 15).
Copyright (c) 2026 saifiwalid.
"""

import statistics


def analyze_market_pricing(products: list[dict], target_price_dzd: int | None = None) -> dict:
    """AGENT 12: Computes median, fair range, and price-per-seat across DZD offers."""
    prices = [p["current_price_dzd"] for p in products if p.get("current_price_dzd")]
    if not prices:
        return {"median_dzd": 0, "fair_min_dzd": 0, "fair_max_dzd": 0, "verdict": "no_data"}

    med = int(statistics.median(prices))
    q1 = int(sorted(prices)[max(0, len(prices) // 4)])
    q3 = int(sorted(prices)[min(len(prices) - 1, (3 * len(prices)) // 4)])

    verdict = "fair"
    if target_price_dzd is not None:
        if target_price_dzd < q1 * 0.75:
            verdict = "suspiciously_low_verify_specs"
        elif target_price_dzd > q3 * 1.25:
            verdict = "above_market_range"
        else:
            verdict = "within_fair_market_range"

    return {
        "agent": "AGENT_12",
        "median_dzd": med,
        "fair_min_dzd": q1,
        "fair_max_dzd": q3,
        "min_dzd": min(prices),
        "max_dzd": max(prices),
        "verdict": verdict,
        "sample_size": len(prices),
    }


def evaluate_seller_trust_signals(seller: dict, product: dict) -> dict:
    """AGENT 14: Reports objective risk indicators without baseless fraud accusations."""
    signals: list[str] = []
    positive_signals: list[str] = []

    if seller.get("has_written_warranty"):
        positive_signals.append("ضمان مكتوب متوفر")
    else:
        signals.append("لا يوجد ضمان مكتوب معلن")

    if seller.get("cash_on_delivery"):
        positive_signals.append("الدفع عند الاستلام متاح")
    else:
        signals.append("الدفع عند الاستلام غير مؤكد")

    if seller.get("business_address"):
        positive_signals.append("عنوان تجاري واضح")
    else:
        signals.append("العنوان التجاري الدقيق غير مذكور")

    if not product.get("foam_density_documented"):
        signals.append("كثافة الرغوة معلنة من البائع وليست موثقة بشهادة")

    if product.get("data_completeness_score", 0) < 60:
        signals.append("اكتمال البيانات التقنية منخفض (< 60%)")

    return {
        "agent": "AGENT_14",
        "trust_score": seller.get("trust_score", 50.0),
        "positive_signals": positive_signals,
        "risk_indicators": signals,
    }


def verify_fact_classification(provenance_fields: list[dict]) -> dict:
    """AGENT 15: Summarizes verification status counts across all fields."""
    counts = {"documented": 0, "seller_claimed": 0, "inferred": 0, "missing": 0, "conflicting": 0}
    for f in provenance_fields:
        st = f.get("verification_status", "missing")
        counts[st] = counts.get(st, 0) + 1
    return {"agent": "AGENT_15", "field_status_counts": counts}


def vision_analysis_guardrail() -> str:
    """AGENT 11: Explicit scientific constraint on visual inference."""
    return (
        "تحليل الصور يحدد الشكل، عدد المقاعد الظاهر، اللون، وتشطيب الخياطة الظاهري فقط. "
        "لا يمكن استنتاج كثافة الرغوة الداخلية أو نوع الخشب الداخلي من الصور الخارجية."
    )
