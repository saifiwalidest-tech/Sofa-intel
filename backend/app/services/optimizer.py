"""Combination Optimization & Pareto Front Engine (AGENT 13).
Finds non-dominated sofa offers balancing price, quality, confidence, and delivery.
Copyright (c) 2026 saifiwalid.
"""


def compute_pareto_front(products: list[dict]) -> list[dict]:
    """Return products on the Pareto Front across:
    - minimize total_cost_dzd
    - maximize quality_score_midpoint
    - maximize evidence_confidence_score
    """
    pareto: list[dict] = []
    for candidate in products:
        dominated = False
        for other in products:
            if other["id"] == candidate["id"]:
                continue
            better_or_equal = (
                other["total_cost_dzd"] <= candidate["total_cost_dzd"]
                and other["quality_score_midpoint"] >= candidate["quality_score_midpoint"]
                and other["evidence_confidence_score"] >= candidate["evidence_confidence_score"]
            )
            strictly_better = (
                other["total_cost_dzd"] < candidate["total_cost_dzd"]
                or other["quality_score_midpoint"] > candidate["quality_score_midpoint"]
                or other["evidence_confidence_score"] > candidate["evidence_confidence_score"]
            )
            if better_or_equal and strictly_better:
                dominated = True
                break
        if not dominated:
            pareto.append(candidate)

    return sorted(pareto, key=lambda x: (-x["value_for_money_score"], x["total_cost_dzd"]))


def classify_tier_recommendations(products: list[dict]) -> dict:
    """Group top offers into Economic, Balanced, and Luxury tiers."""
    if not products:
        return {"economic": [], "balanced": [], "luxury": []}

    economic = sorted(
        [p for p in products if p["total_cost_dzd"] <= 110000],
        key=lambda x: (-x["value_for_money_score"], x["total_cost_dzd"]),
    )[:3]
    balanced = sorted(
        [p for p in products if 95000 <= p["total_cost_dzd"] <= 170000],
        key=lambda x: (-x["quality_score_midpoint"], -x["value_for_money_score"]),
    )[:3]
    luxury = sorted(
        [p for p in products if p["quality_score_midpoint"] >= 75],
        key=lambda x: (-x["quality_score_midpoint"], -x["evidence_confidence_score"]),
    )[:3]

    return {"economic": economic, "balanced": balanced, "luxury": luxury}
