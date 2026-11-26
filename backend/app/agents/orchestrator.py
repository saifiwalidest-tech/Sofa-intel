"""AGENT 00 — Master Orchestrator.
Coordinates internal domain, verification, and sofa-category specialists.
Copyright (c) 2026 saifiwalid.
"""

from app.agents.domain_experts import (
    analyze_foam_engineering,
    analyze_wood_engineering,
    analyze_upholstery_suspension,
    classify_seller_channel,
)
from app.agents.sofa_specialists import analyze_sofa_category_specialist
from app.agents.verification_trust import (
    evaluate_seller_trust_signals,
    verify_fact_classification,
    vision_analysis_guardrail,
)


def run_product_intelligence_pipeline(product_dict: dict) -> dict:
    """Run all internal engineering, category-specialist, and verification modules."""
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
    category_report = analyze_sofa_category_specialist(
        product_dict.get("sofa_type", "modern"),
        product_dict.get("foam_density_claimed"),
        product_dict.get("wood_type"),
    )
    channel_report = classify_seller_channel(seller.get("seller_type", "retailer"))
    trust_report = evaluate_seller_trust_signals(seller, product_dict)
    fact_report = verify_fact_classification(product_dict.get("provenance_fields", []))

    return {
        "channel_analysis": channel_report,
        "foam_analysis": foam_report,
        "wood_analysis": wood_report,
        "upholstery_analysis": upholstery_report,
        "category_specialist": category_report,
        "trust_analysis": trust_report,
        "fact_checking": fact_report,
        "vision_guardrail": vision_analysis_guardrail(),
    }
