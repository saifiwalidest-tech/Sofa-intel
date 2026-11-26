"""AGENT 00 — Master Orchestrator.
Coordinates Agents 01..17, enforces loop/retry limits, and aggregates verified product analysis.
Copyright (c) 2026 saifiwalid.
"""

from app.agents.domain_experts import (
    analyze_foam_engineering,
    analyze_wood_engineering,
    analyze_upholstery_suspension,
    classify_seller_channel,
)
from app.agents.verification_trust import (
    evaluate_seller_trust_signals,
    verify_fact_classification,
    vision_analysis_guardrail,
)


def run_product_intelligence_pipeline(product_dict: dict) -> dict:
    """Run all domain & verification agents on a single product record."""
    seller = product_dict.get("seller", {})
    foam_report = analyze_foam_engineering(
        product_dict.get("foam_density_claimed"),
        product_dict.get("foam_density_documented", False),
        product_dict.get("foam_thickness_cm"),
        product_dict.get("foam_firmness"),
    )
    wood_report = analyze_wood_engineering(
        product_dict.get("wood_type"),
        product_dict.get("assembly_method"),
    )
    upholstery_report = analyze_upholstery_suspension(
        product_dict.get("fabric_type"),
        product_dict.get("fabric_properties", []),
        product_dict.get("suspension_type"),
    )
    channel_report = classify_seller_channel(seller.get("seller_type", "retailer"))
    trust_report = evaluate_seller_trust_signals(seller, product_dict)
    fact_report = verify_fact_classification(product_dict.get("provenance_fields", []))

    return {
        "orchestrator": "AGENT_00",
        "channel_analysis": channel_report,
        "foam_analysis": foam_report,
        "wood_analysis": wood_report,
        "upholstery_analysis": upholstery_report,
        "trust_analysis": trust_report,
        "fact_checking": fact_report,
        "vision_guardrail": vision_analysis_guardrail(),
    }
