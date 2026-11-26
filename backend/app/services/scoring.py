"""Sofa Quality Index & Multi-Dimensional Scoring Engine (AGENT 08, 09, 10, 12, 13, 15).
Strictly preserves missing fields without assigning 0; computes min..max quality intervals.
Copyright (c) 2026 saifiwalid.
"""

from app.schemas import CustomWeights

FOAM_BASE_SCORES: dict[str, float] = {
    "HR": 92.0,
    "D50": 90.0,
    "D45": 88.0,
    "D40": 85.0,
    "D36": 80.0,
    "D35": 77.0,
    "Memory": 82.0,
    "D32": 68.0,
    "D30": 62.0,
    "D28": 55.0,
    "D25": 46.0,
    "D20": 35.0,
    "Rebonded": 58.0,
}

WOOD_BASE_SCORES: dict[str, float] = {
    "Hêtre": 92.0,
    "Chêne": 94.0,
    "Massif": 88.0,
    "Pin": 72.0,
    "Sapin": 68.0,
    "Metal": 78.0,
    "Contreplaqué": 60.0,
    "OSB": 48.0,
    "MDF": 42.0,
    "Aggloméré": 32.0,
}

FABRIC_BASE_SCORES: dict[str, float] = {
    "Tissu anti-tache": 90.0,
    "Tissu déperlant": 88.0,
    "Cuir": 92.0,
    "Microfibre": 82.0,
    "Chenille": 80.0,
    "Bouclé": 78.0,
    "Velours": 76.0,
    "Lin": 74.0,
    "Jacquard": 72.0,
    "Simili cuir": 55.0,
}

SUSPENSION_BASE_SCORES: dict[str, float] = {
    "Ressorts ensachés + sangles": 92.0,
    "Ressorts Nosag": 86.0,
    "Ressorts métalliques": 82.0,
    "Sangles élastiques renforcées": 70.0,
    "Sangles simples": 52.0,
}


def compute_product_scores(
    *,
    foam_density_claimed: str | None,
    foam_density_documented: bool,
    foam_thickness_cm: float | None,
    wood_type: str | None,
    assembly_method: str | None,
    fabric_type: str | None,
    fabric_properties: list[str],
    suspension_type: str | None,
    seller_type: str,
    warranty_months: int | None,
    current_price_dzd: int,
    delivery_cost_dzd: int | None,
    has_written_warranty: bool,
    provides_invoice: bool,
    weights: CustomWeights | None = None,
) -> dict:
    w = weights or CustomWeights()
    total_w = max(w.foam + w.structure + w.upholstery + w.suspension + w.craftsmanship + w.warranty, 1.0)

    # Track known vs missing dimensions (6 core dimensions)
    known_dims = 0
    total_dims = 6
    documented_count = 0

    # 1. Foam (0..100 normalized)
    if foam_density_claimed:
        known_dims += 1
        base = FOAM_BASE_SCORES.get(foam_density_claimed.upper(), 60.0)
        if foam_thickness_cm and foam_thickness_cm >= 14:
            base = min(100.0, base + 5.0)
        if foam_density_documented:
            documented_count += 1
            foam_min, foam_max = base, min(100.0, base + 3.0)
        else:
            # Unverified claim has wider uncertainty interval
            foam_min, foam_max = max(35.0, base - 18.0), base
    else:
        foam_min, foam_max = 30.0, 85.0

    # 2. Structure / Wood
    if wood_type:
        known_dims += 1
        w_base = 65.0
        for k, v in WOOD_BASE_SCORES.items():
            if k.lower() in wood_type.lower():
                w_base = v
                break
        if assembly_method and ("tenon" in assembly_method.lower() or "renforc" in assembly_method.lower() or "مدعم" in assembly_method):
            w_base = min(100.0, w_base + 5.0)
            documented_count += 1
        struct_min, struct_max = max(30.0, w_base - 8.0), w_base
    else:
        struct_min, struct_max = 30.0, 85.0

    # 3. Upholstery / Fabric
    if fabric_type:
        known_dims += 1
        f_base = 70.0
        for k, v in FABRIC_BASE_SCORES.items():
            if k.lower() in fabric_type.lower():
                f_base = v
                break
        if any("anti" in p.lower() or "déperlant" in p.lower() or "غسل" in p for p in fabric_properties):
            f_base = min(100.0, f_base + 6.0)
        fab_min, fab_max = max(40.0, f_base - 6.0), f_base
    else:
        fab_min, fab_max = 40.0, 85.0

    # 4. Suspension
    if suspension_type:
        known_dims += 1
        s_base = 68.0
        for k, v in SUSPENSION_BASE_SCORES.items():
            if k.lower() in suspension_type.lower():
                s_base = v
                break
        susp_min, susp_max = max(40.0, s_base - 6.0), s_base
    else:
        susp_min, susp_max = 35.0, 85.0

    # 5. Craftsmanship (factory direct & assembly info)
    known_dims += 1
    craft_base = 82.0 if seller_type in ("direct_factory", "artisan_workshop") else 68.0
    craft_min, craft_max = craft_base - 5.0, min(100.0, craft_base + 8.0)

    # 6. Warranty & After-Sales
    if warranty_months is not None:
        known_dims += 1
        war_base = min(100.0, 40.0 + warranty_months * 2.5)
        if has_written_warranty:
            war_base = min(100.0, war_base + 10.0)
            documented_count += 1
        if provides_invoice:
            war_base = min(100.0, war_base + 5.0)
        war_min, war_max = max(30.0, war_base - 5.0), war_base
    else:
        war_min, war_max = 20.0, 75.0

    q_min = (
        foam_min * w.foam
        + struct_min * w.structure
        + fab_min * w.upholstery
        + susp_min * w.suspension
        + craft_min * w.craftsmanship
        + war_min * w.warranty
    ) / total_w

    q_max = (
        foam_max * w.foam
        + struct_max * w.structure
        + fab_max * w.upholstery
        + susp_max * w.suspension
        + craft_max * w.craftsmanship
        + war_max * w.warranty
    ) / total_w

    q_mid = round((q_min + q_max) / 2.0, 1)
    completeness = round((known_dims / total_dims) * 100.0, 1)
    evidence_confidence = round(min(100.0, (completeness * 0.65) + (documented_count / 3.0) * 35.0), 1)

    total_cost = current_price_dzd + (delivery_cost_dzd or 0)
    # Value for money: quality per 100k DZD normalized to 0..100
    price_factor = max(total_cost / 100000.0, 0.35)
    value_score = round(min(100.0, max(10.0, (q_mid / price_factor) * 0.85)), 1)

    comfort_score = round((foam_max * 0.55 + fab_max * 0.25 + susp_max * 0.20), 1)
    deliv_score = 95.0 if (delivery_cost_dzd is not None and delivery_cost_dzd <= 3000) else (
        75.0 if (delivery_cost_dzd is not None and delivery_cost_dzd <= 7000) else 50.0
    )

    return {
        "quality_score_min": round(q_min, 1),
        "quality_score_max": round(q_max, 1),
        "quality_score_midpoint": q_mid,
        "value_for_money_score": value_score,
        "evidence_confidence_score": evidence_confidence,
        "data_completeness_score": completeness,
        "comfort_suitability_score": comfort_score,
        "delivery_cost_score": deliv_score,
    }
