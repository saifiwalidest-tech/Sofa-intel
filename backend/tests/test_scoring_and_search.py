"""Unit tests for Sofa Quality Index, missing data ranges, multilingual search & price normalization.
Copyright (c) 2026 saifiwalid.
"""

from app.agents.consultant import parse_consultant_intent
from app.services.multilingual_search import expand_multilingual_query, normalize_algerian_price_to_dzd
from app.services.optimizer import compute_pareto_front
from app.services.scoring import compute_product_scores


def test_missing_data_produces_interval_not_zero():
    partial = compute_product_scores(
        foam_density_claimed="D36",
        foam_density_documented=False,
        foam_thickness_cm=None,
        wood_type=None,
        assembly_method=None,
        fabric_type="Velours",
        fabric_properties=[],
        suspension_type=None,
        seller_type="retailer",
        warranty_months=None,
        current_price_dzd=120000,
        delivery_cost_dzd=3000,
        has_written_warranty=False,
        provides_invoice=False,
    )
    assert partial["quality_score_min"] > 0
    assert partial["quality_score_max"] > partial["quality_score_min"]
    assert partial["data_completeness_score"] < 100.0


def test_documented_foam_scores_higher_confidence_than_claimed():
    doc = compute_product_scores(
        foam_density_claimed="D36",
        foam_density_documented=True,
        foam_thickness_cm=16.0,
        wood_type="Hêtre",
        assembly_method="Tenon et mortaise renforcé",
        fabric_type="Tissu anti-tache",
        fabric_properties=["anti-tache"],
        suspension_type="Ressorts Nosag",
        seller_type="direct_factory",
        warranty_months=24,
        current_price_dzd=115000,
        delivery_cost_dzd=2500,
        has_written_warranty=True,
        provides_invoice=True,
    )
    unverified = compute_product_scores(
        foam_density_claimed="D36",
        foam_density_documented=False,
        foam_thickness_cm=16.0,
        wood_type="Hêtre",
        assembly_method="Tenon et mortaise renforcé",
        fabric_type="Tissu anti-tache",
        fabric_properties=["anti-tache"],
        suspension_type="Ressorts Nosag",
        seller_type="direct_factory",
        warranty_months=24,
        current_price_dzd=115000,
        delivery_cost_dzd=2500,
        has_written_warranty=True,
        provides_invoice=True,
    )
    assert doc["evidence_confidence_score"] > unverified["evidence_confidence_score"]
    assert doc["quality_score_min"] > unverified["quality_score_min"]


def test_centimes_to_dzd_normalization():
    price, status = normalize_algerian_price_to_dzd("عندي ميزانية 12 مليون سنتيم")
    assert price == 120000
    assert status == "normalized_from_centimes"


def test_multilingual_query_expansion():
    tokens = expand_multilingual_query("صالون موس 36 خشب الزان")
    assert "d36" in tokens
    assert "hêtre" in tokens


def test_consultant_darja_parsing():
    intent = parse_consultant_intent(
        "عندي ميزانية 12 مليون سنتيم، نحب صالون L برغوة D36 وخشب الزان، قريب للبليدة، وما يكونش القماش يتوسخ بسرعة"
    )
    assert intent["budget_dzd"] == 120000
    assert intent["sofa_type"] == "l_shape"
    assert intent["foam_density"] == "D36"
    assert intent["wood_type"] == "Hêtre"
    assert intent["wilaya_code"] == "09"
    assert intent["stain_resistant"] is True


def test_pareto_front_filters_dominated_items():
    items = [
        {"id": "a", "total_cost_dzd": 100000, "quality_score_midpoint": 85.0, "evidence_confidence_score": 90.0, "value_for_money_score": 80.0},
        {"id": "b", "total_cost_dzd": 130000, "quality_score_midpoint": 70.0, "evidence_confidence_score": 70.0, "value_for_money_score": 50.0},
    ]
    front = compute_pareto_front(items)
    assert [x["id"] for x in front] == ["a"]
