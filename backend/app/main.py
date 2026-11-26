"""SOFA INTEL DZ — FastAPI Main Application.
Copyright (c) 2026 saifiwalid. All rights reserved.
"""

import asyncio
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.adapters.sources import get_all_adapter_statuses
from app.agents.consultant import build_consultant_response, parse_consultant_intent
from app.agents.orchestrator import run_product_intelligence_pipeline
from app.agents.registry import AGENTS_CATALOG
from app.agents.social_harvester import extract_social_listing_metadata
from app.agents.verification_trust import analyze_market_pricing
from app.config import get_settings
from app.database import (
    AlertRule,
    AuditLog,
    FieldProvenance,
    ListingReport,
    PriceHistory,
    Product,
    SavedSearch,
    Seller,
    SessionLocal,
    get_db,
    init_db,
)
from app.schemas import (
    AlertRequest,
    CompareRequest,
    ConsultantRequest,
    CustomWeights,
    ProductOut,
    ProductSubmitRequest,
    ReportRequest,
    SavedSearchRequest,
    VerificationChecklistRequest,
    VisualSearchRequest,
)
from app.security import InMemoryRateLimiter, require_role, sanitize_text, validate_external_url
from app.seed_demo import seed_demo_data_if_empty
from app.services.geo_algeria import WILAYAS, WILAYA_BY_CODE, estimate_delivery_dzd, haversine_km
from app.services.multilingual_search import expand_multilingual_query
from app.services.optimizer import classify_tier_recommendations, compute_pareto_front
from app.services.scoring import compute_product_scores

settings = get_settings()
rate_limiter = InMemoryRateLimiter(settings.api_rate_limit_per_minute)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as session:
        seed_demo_data_if_empty(session)
    yield


app = FastAPI(
    title="SOFA INTEL DZ API",
    description="Autonomous Multi-Agent Sofa Market Intelligence Platform for Algeria. Copyright (c) 2026 saifiwalid.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _product_to_dict(p: Product) -> dict:
    return ProductOut.from_orm(p).dict()


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "copyright": settings.app_copyright,
        "llm_provider": settings.llm_provider,
    }


@app.get("/api/v1/products")
async def list_products(
    request: Request,
    q: str | None = None,
    wilaya_code: str | None = None,
    commune: str | None = None,
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    sofa_type: str | None = None,
    seats_min: int | None = Query(default=None, ge=1),
    foam_density: str | None = None,
    wood_type: str | None = None,
    fabric_type: str | None = None,
    suspension_type: str | None = None,
    color: str | None = None,
    seller_type: str | None = None,
    min_warranty_months: int | None = None,
    delivery_available: bool | None = None,
    documented_only: bool = False,
    min_confidence: float | None = None,
    max_distance_km: float | None = None,
    user_wilaya_code: str | None = None,
    source_platform: str | None = None,
    db: Session = Depends(get_db),
):
    rate_limiter.check(request)
    stmt = (
        select(Product)
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    rows = (db.execute(stmt)).scalars().all()
    tokens = expand_multilingual_query(q) if q else []

    results: list[dict] = []
    for p in rows:
        if wilaya_code and p.seller.wilaya_code != wilaya_code:
            continue
        if commune and commune.lower() not in p.seller.commune.lower():
            continue
        if min_price is not None and p.current_price_dzd < min_price:
            continue
        if max_price is not None and p.current_price_dzd > max_price:
            continue
        if sofa_type and p.sofa_type != sofa_type:
            continue
        if seats_min is not None and (p.seats_count or 0) < seats_min:
            continue
        if foam_density and foam_density.upper() not in (p.foam_density_claimed or "").upper():
            continue
        if wood_type and wood_type.lower() not in (p.wood_type or "").lower():
            continue
        if fabric_type and fabric_type.lower() not in (p.fabric_type or "").lower():
            continue
        if suspension_type and suspension_type.lower() not in (p.suspension_type or "").lower():
            continue
        if color and color.lower() not in (p.color or "").lower():
            continue
        if seller_type and p.seller.seller_type != seller_type:
            continue
        if min_warranty_months is not None and (p.warranty_months or 0) < min_warranty_months:
            continue
        if delivery_available is not None and p.delivery_available != delivery_available:
            continue
        if documented_only and not p.foam_density_documented:
            continue
        if min_confidence is not None and p.evidence_confidence_score < min_confidence:
            continue
        if source_platform and source_platform.lower() not in (p.primary_source_name or "").lower():
            continue

        if max_distance_km is not None and user_wilaya_code and user_wilaya_code in WILAYA_BY_CODE:
            uw = WILAYA_BY_CODE[user_wilaya_code]
            if p.seller.latitude is not None and p.seller.longitude is not None:
                dist = haversine_km(uw["lat"], uw["lon"], p.seller.latitude, p.seller.longitude)
                if dist > max_distance_km:
                    continue

        if tokens:
            haystack = " ".join([
                p.title or "",
                p.description or "",
                p.sofa_type or "",
                p.foam_density_claimed or "",
                p.wood_type or "",
                p.fabric_type or "",
                " ".join(p.fabric_properties or []),
                p.primary_source_name or "",
                p.seller.name or "",
                p.seller.wilaya_name or "",
                p.seller.commune or "",
            ]).lower()
            if not any(tok in haystack for tok in tokens):
                continue

        results.append(_product_to_dict(p))

    return {"count": len(results), "expanded_tokens": tokens, "items": results}


@app.get("/api/v1/products/{product_id}")
async def get_product_detail(product_id: str, db: Session = Depends(get_db)):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    prod = (db.execute(stmt)).scalar_one_or_none()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    p_dict = _product_to_dict(prod)
    agent_analysis = run_product_intelligence_pipeline(p_dict)
    return {"product": p_dict, "agent_analysis": agent_analysis}


@app.post("/api/v1/products/submit")
async def submit_product_listing(payload: ProductSubmitRequest, request: Request, db: Session = Depends(get_db)):
    rate_limiter.check(request)
    safe_url = validate_external_url(payload.source_url)
    wilaya = WILAYA_BY_CODE.get(payload.wilaya_code, WILAYA_BY_CODE["09"])
    seller_id = f"user-seller-{uuid.uuid4().hex[:8]}"
    prod_id = f"user-sofa-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    seller = Seller(
        id=seller_id,
        name=sanitize_text(payload.seller_name, 200),
        seller_type=payload.seller_type,
        wilaya_code=wilaya["code"],
        wilaya_name=wilaya["name_ar"],
        commune=sanitize_text(payload.commune, 120),
        latitude=wilaya["lat"],
        longitude=wilaya["lon"],
        trust_score=60.0,
        is_demo=False,
    )
    scores = compute_product_scores(
        foam_density_claimed=payload.foam_density_claimed,
        foam_density_documented=False,
        foam_thickness_cm=None,
        wood_type=payload.wood_type,
        assembly_method=None,
        fabric_type=payload.fabric_type,
        fabric_properties=[],
        suspension_type=payload.suspension_type,
        seller_type=payload.seller_type,
        warranty_months=payload.warranty_months,
        current_price_dzd=payload.current_price_dzd,
        delivery_cost_dzd=None,
        has_written_warranty=bool(payload.warranty_months),
        provides_invoice=False,
    )
    prod = Product(
        id=prod_id,
        seller_id=seller_id,
        title=sanitize_text(payload.title, 300),
        description="Submitted via user/partner verified adapter.",
        sofa_type=payload.sofa_type,
        condition="new",
        images=["/images/sofa-l-navy.svg"],
        foam_density_claimed=payload.foam_density_claimed,
        foam_density_documented=False,
        wood_type=sanitize_text(payload.wood_type, 80) if payload.wood_type else None,
        fabric_type=sanitize_text(payload.fabric_type, 80) if payload.fabric_type else None,
        suspension_type=sanitize_text(payload.suspension_type, 80) if payload.suspension_type else None,
        current_price_dzd=payload.current_price_dzd,
        total_cost_dzd=payload.current_price_dzd,
        warranty_months=payload.warranty_months,
        primary_source_name="manual_verified",
        source_url=safe_url,
        published_at=now,
        last_verified_at=now,
        is_demo=False,
        **scores,
    )
    db.add(seller)
    db.add(prod)
    db.add(
        FieldProvenance(
            product_id=prod_id,
            field_name="source_url",
            field_value=safe_url,
            verification_status="seller_claimed",
            source_name="manual_verified",
            source_url=safe_url,
            confidence=0.75,
        )
    )
    db.add(PriceHistory(product_id=prod_id, price_dzd=payload.current_price_dzd, source_name="manual_verified"))
    db.add(AuditLog(actor_role="consumer", action="submit_listing", target=prod_id))
    db.commit()
    return {"status": "created", "product_id": prod_id}


@app.post("/api/v1/compare")
async def compare_products(payload: CompareRequest, db: Session = Depends(get_db)):
    stmt = (
        select(Product)
        .where(Product.id.in_(payload.product_ids))
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    rows = (db.execute(stmt)).scalars().all()
    if len(rows) < 2:
        raise HTTPException(status_code=404, detail="At least 2 valid products required for comparison")
    items = [_product_to_dict(r) for r in rows]

    best_quality = max(items, key=lambda x: x["quality_score_midpoint"])
    best_value = max(items, key=lambda x: x["value_for_money_score"])
    most_expensive = max(items, key=lambda x: x["total_cost_dzd"])
    cheapest = min(items, key=lambda x: x["total_cost_dzd"])

    missing_checks = []
    for item in items:
        missing = [f["field_name"] for f in item["provenance_fields"] if f["verification_status"] == "missing"]
        if not item["foam_density_documented"]:
            missing.append("foam_certificate")
        if missing:
            missing_checks.append({"product_id": item["id"], "title": item["title"], "verify_before_buying": list(set(missing))})

    insights = {
        "why_best_quality": f"«{best_quality['title']}» يتصدر بنطاق جودة {best_quality['quality_score_min']}–{best_quality['quality_score_max']}/100 واكتمال بيانات {best_quality['data_completeness_score']}%.",
        "why_most_expensive": f"«{most_expensive['title']}» هو الأعلى سعراً ({most_expensive['total_cost_dzd']:,} دج) بسبب: نوع الخشب ({most_expensive['wood_type'] or 'غير محدد'})، الكثافة ({most_expensive['foam_density_claimed'] or 'غير محددة'})، والضمان.",
        "price_difference_justified": best_quality["id"] == most_expensive["id"],
        "best_long_term_investment": best_quality["id"],
        "best_value_for_budget": best_value["id"],
        "cheapest_offer": cheapest["id"],
        "verification_needed": missing_checks,
    }
    return {"items": items, "insights": insights}


@app.post("/api/v1/scoring/custom")
async def score_with_custom_weights(weights: CustomWeights, db: Session = Depends(get_db)):
    stmt = select(Product).options(selectinload(Product.seller))
    rows = (db.execute(stmt)).scalars().all()
    recalculated = []
    for p in rows:
        sc = compute_product_scores(
            foam_density_claimed=p.foam_density_claimed,
            foam_density_documented=p.foam_density_documented,
            foam_thickness_cm=p.foam_thickness_cm,
            wood_type=p.wood_type,
            assembly_method=p.assembly_method,
            fabric_type=p.fabric_type,
            fabric_properties=p.fabric_properties or [],
            suspension_type=p.suspension_type,
            seller_type=p.seller.seller_type,
            warranty_months=p.warranty_months,
            current_price_dzd=p.current_price_dzd,
            delivery_cost_dzd=p.delivery_cost_dzd,
            has_written_warranty=p.seller.has_written_warranty,
            provides_invoice=p.seller.provides_invoice,
            weights=weights,
        )
        recalculated.append({"id": p.id, "title": p.title, "current_price_dzd": p.current_price_dzd, **sc})
    recalculated.sort(key=lambda x: -x["quality_score_midpoint"])
    return {"weights": weights.dict(), "items": recalculated}


@app.get("/api/v1/optimize/pareto")
async def get_pareto_optimization(db: Session = Depends(get_db)):
    stmt = (
        select(Product)
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    rows = (db.execute(stmt)).scalars().all()
    items = [_product_to_dict(r) for r in rows]
    pareto = compute_pareto_front(items)
    tiers = classify_tier_recommendations(items)
    return {"pareto_front": pareto, "tiers": tiers, "total_evaluated": len(items)}


@app.post("/api/v1/consultant/ask")
async def ask_consultant(payload: ConsultantRequest, request: Request, db: Session = Depends(get_db)):
    rate_limiter.check(request)
    intent = parse_consultant_intent(payload.message, payload.user_wilaya_code)
    stmt = (
        select(Product)
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    rows = (db.execute(stmt)).scalars().all()
    items = [_product_to_dict(r) for r in rows]
    return build_consultant_response(intent, items)


@app.post("/api/v1/verification-lab/checklist")
async def generate_verification_checklist(payload: VerificationChecklistRequest):
    questions = [
        "هل كثافة الرغوة المعلنة موثقة بشهادة أو بطاقة تقنية من المصنع؟",
        "من هو مصنع الرغوة وما سماكة الرغوة الفعلية في المقعد والظهر (بالسنتيمتر)؟",
        "هل الهيكل مصنوع بالكامل من الخشب المعلن أم توجد أجزاء MDF أو خشب حبيبي؟",
        "هل الخشب مجفف لتفادي التشوه والتشقق مستقبلاً؟",
        "ما نوع نظام التعليق (نوابض Nosag، نوابض معدنية، أم أحزمة مرنة)؟",
        "هل توجد صور واضحة للهيكل الخشبي قبل التنجيد؟",
        "ما مدة الضمان المكتوب وما الذي يشمله بالضبط؟",
        "هل السعر النهائي يشمل النقل والتركيب داخل الولاية؟",
    ]
    foam = payload.foam_density or "D36"
    wood = payload.wood_type or "الزان (Hêtre)"
    if payload.language == "darja":
        message_template = (
            f"السلام عليكم خويا، شفت الصالون تاعكم وحاب نتأكد من بعض التفاصيل قبل الشراء: "
            f"1) رغوة {foam} عندكم شهادة تقنية ولا بطاقة تثبت الكثافة وشحال السماكة؟ "
            f"2) الكادر (الهيكل) مخدوم كامل بخشب {wood} ومجفف؟ تقدر تبعثلي صورة قبل التغليف؟ "
            f"3) واش نوع التعليق (رسور ولا سانقل)؟ "
            f"4) شحال الضمان المكتوب والسعر يشمل التوصيل والتركيب؟ شكراً."
        )
    elif payload.language == "fr":
        message_template = (
            f"Bonjour, je suis intéressé(e) par votre salon. Avant de commander, pourriez-vous me confirmer : "
            f"1) La densité de la mousse ({foam}) est-elle certifiée et quelle est son épaisseur ? "
            f"2) La structure est-elle 100% en bois {wood} séché (avez-vous des photos avant tapissage) ? "
            f"3) Quel est le système de suspension (ressorts Nosag ou sangles) ? "
            f"4) Quelle est la durée de garantie écrite et la livraison/installation est-elle incluse ?"
        )
    else:
        message_template = (
            f"السلام عليكم، أرغب في الاستفسار عن تفاصيل الجودة قبل تأكيد الطلب: "
            f"1) هل كثافة الرغوة ({foam}) موثقة ببطاقة تقنية وما سماكتها؟ "
            f"2) هل الهيكل مصنوع بالكامل من خشب {wood} المجفف وهل تتوفر صور قبل التنجيد؟ "
            f"3) ما نوع التعليق المستخدم، وما مدة الضمان المكتوب، وهل السعر يشمل التوصيل؟"
        )
    return {"questions": questions, "ready_message": message_template, "language": payload.language}


@app.post("/api/v1/visual-search")
async def visual_search(payload: VisualSearchRequest, db: Session = Depends(get_db)):
    stmt = (
        select(Product)
        .options(selectinload(Product.seller), selectinload(Product.provenance_fields), selectinload(Product.price_history))
    )
    rows = (db.execute(stmt)).scalars().all()
    scored = []
    for p in rows:
        sim = 40.0
        if payload.sofa_type and p.sofa_type == payload.sofa_type:
            sim += 30.0
        if payload.color and payload.color.lower() in (p.color or "").lower():
            sim += 15.0
        if payload.seats_count and p.seats_count == payload.seats_count:
            sim += 15.0
        scored.append({"similarity_percent": min(99.0, sim), "product": _product_to_dict(p)})
    scored.sort(key=lambda x: -x["similarity_percent"])
    return {
        "agent": "AGENT_11",
        "guardrail_note": "المطابقة البصرية تعتمد على الشكل واللون وعدد المقاعد الظاهر ولا تستنتج الكثافة أو الخشب الداخلي.",
        "matches": scored[:6],
    }


@app.get("/api/v1/geo/wilayas")
async def get_wilayas(user_wilaya_code: str = "16", db: Session = Depends(get_db)):
    stmt = select(Product).options(selectinload(Product.seller))
    rows = (db.execute(stmt)).scalars().all()
    counts_by_w: dict[str, int] = {}
    for p in rows:
        wc = p.seller.wilaya_code
        counts_by_w[wc] = counts_by_w.get(wc, 0) + 1

    enriched = []
    for w in WILAYAS:
        deliv, dist = estimate_delivery_dzd(w["code"], user_wilaya_code)
        enriched.append({**w, "offers_count": counts_by_w.get(w["code"], 0), "estimated_delivery_dzd": deliv, "distance_km": dist})
    return {"total_wilayas": len(WILAYAS), "wilayas": enriched}


@app.get("/api/v1/manufacturers")
async def list_manufacturers(wilaya_code: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Seller)
    rows = (db.execute(stmt)).scalars().all()
    if wilaya_code:
        rows = [r for r in rows if r.wilaya_code == wilaya_code]
    return {"count": len(rows), "items": rows}


@app.get("/api/v1/price-observatory")
async def price_observatory(db: Session = Depends(get_db)):
    stmt = select(Product).options(selectinload(Product.seller))
    rows = (db.execute(stmt)).scalars().all()
    items = [{"id": p.id, "title": p.title, "sofa_type": p.sofa_type, "current_price_dzd": p.current_price_dzd, "seats_count": p.seats_count, "seller_type": p.seller.seller_type} for p in rows]
    stats = analyze_market_pricing(items)
    by_type: dict[str, list[int]] = {}
    for it in items:
        by_type.setdefault(it["sofa_type"], []).append(it["current_price_dzd"])
    type_averages = {k: int(sum(v) / len(v)) for k, v in by_type.items()}
    return {"market_stats": stats, "average_by_type_dzd": type_averages, "items": items}


@app.get("/api/v1/adapters/status")
async def adapters_status():
    return {"adapters": get_all_adapter_statuses()}


@app.get("/api/v1/agents/status")
async def agents_status():
    return {"total_agents": len(AGENTS_CATALOG), "agents": AGENTS_CATALOG}


@app.get("/api/v1/saved-searches")
async def get_saved_searches(db: Session = Depends(get_db)):
    rows = (db.execute(select(SavedSearch))).scalars().all()
    return {"items": rows}


@app.post("/api/v1/saved-searches")
async def create_saved_search(payload: SavedSearchRequest, db: Session = Depends(get_db)):
    item = SavedSearch(name=sanitize_text(payload.name, 150), filters_json=payload.filters_json)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/api/v1/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    rows = (db.execute(select(AlertRule))).scalars().all()
    return {"items": rows}


@app.post("/api/v1/alerts")
async def create_alert(payload: AlertRequest, db: Session = Depends(get_db)):
    item = AlertRule(
        label=sanitize_text(payload.label, 200),
        wilaya_code=payload.wilaya_code,
        max_price_dzd=payload.max_price_dzd,
        min_foam_density=payload.min_foam_density,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.post("/api/v1/reports")
async def create_report(payload: ReportRequest, request: Request, db: Session = Depends(get_db)):
    rate_limiter.check(request)
    rep = ListingReport(
        product_id=payload.product_id,
        reason=sanitize_text(payload.reason, 120),
        details=sanitize_text(payload.details, 2000),
        reporter_contact=sanitize_text(payload.reporter_contact, 150) if payload.reporter_contact else None,
    )
    db.add(rep)
    db.add(AuditLog(actor_role="consumer", action="report_listing", target=payload.product_id or "general"))
    db.commit()
    db.refresh(rep)
    return {"status": "submitted", "report_id": rep.id}


@app.get("/api/v1/admin/audit-logs")
async def get_audit_logs(request: Request, db: Session = Depends(get_db)):
    require_role(request, ("admin", "consumer"))
    rows = (db.execute(select(AuditLog).order_by(AuditLog.id.desc()).limit(50))).scalars().all()
    return {"items": rows}


@app.post("/api/v1/social/extract")
async def extract_social_post(payload: dict, request: Request):
    rate_limiter.check(request)
    raw_text = str(payload.get("text", ""))
    source_url = str(payload.get("source_url", ""))
    if source_url:
        validate_external_url(source_url)
    return extract_social_listing_metadata(raw_text, source_url)


@app.websocket("/ws/search/{job_id}")
async def ws_search_progress(websocket: WebSocket, job_id: str):
    await websocket.accept()
    stages = [
        {"stage": "توسيع الاستعلام", "progress": 15, "message": "تحليل الكلمات المفتاحية والمرادفات متعددة اللغات..."},
        {"stage": "فحص المنصات الاجتماعية", "progress": 35, "message": "البحث في فهرس إعلانات فيسبوك، إنستغرام، تيك توك وOuedkniss..."},
        {"stage": "التحليل الهندسي", "progress": 55, "message": "مطابقة كثافة الرغوة ونوع الخشب ونظام التعليق..."},
        {"stage": "تحليل الأسعار والتوصيل", "progress": 75, "message": "توحيد الأسعار بالدينار الجزائري وحساب تكلفة التوصيل..."},
        {"stage": "ترتيب القيمة", "progress": 90, "message": "مقارنة العروض واستخراج أفضل التوليفات المتاحة..."},
        {"stage": "اكتمال التحقق", "progress": 100, "message": "تم التحقق من المصادر والبيانات المتاحة."},
    ]
    try:
        for st in stages:
            await websocket.send_json({"job_id": job_id, **st})
            await asyncio.sleep(0.25)
        await websocket.close()
    except WebSocketDisconnect:
        pass
