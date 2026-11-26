"""Domain Expert Agents: AGENT 06 (Manufacturer), AGENT 08 (Foam), AGENT 09 (Wood), AGENT 10 (Upholstery).
Copyright (c) 2026 saifiwalid.
"""


def analyze_foam_engineering(
    density_claimed: str | None,
    documented: bool,
    thickness_cm: float | None,
    firmness: str | None,
) -> dict:
    """AGENT 08: Never assumes D36 means true 36 kg/m³ without technical documentation."""
    if not density_claimed:
        return {
            "agent": "AGENT_08",
            "status": "missing",
            "summary": "كثافة الرغوة غير مذكورة في الإعلان؛ يجب سؤال البائع عن الكثافة الحقيقية والشهادة التقنية.",
            "verification_warning": True,
        }
    verdict = "موثقة بشهادة تقنية" if documented else "ادعاء تسويقي من البائع فقط (غير موثق بشهادة)"
    suitability = "ممتازة للاستخدام العائلي اليومي" if density_claimed.upper() in ("D36", "D40", "D45", "D50", "HR") else "مناسبة للاستخدام المتوسط أو الضيوف"
    return {
        "agent": "AGENT_08",
        "status": "documented" if documented else "seller_claimed",
        "density_claimed": density_claimed,
        "thickness_cm": thickness_cm,
        "firmness": firmness or "غير محددة",
        "suitability": suitability,
        "summary": f"رغوة {density_claimed} ({verdict}). {suitability}.",
        "verification_warning": not documented,
    }


def analyze_wood_engineering(wood_type: str | None, assembly_method: str | None) -> dict:
    """AGENT 09: Evaluates wood + assembly; never judges durability by wood name alone."""
    if not wood_type:
        return {
            "agent": "AGENT_09",
            "status": "missing",
            "summary": "نوع الخشب غير مذكور؛ اطلب صوراً للهيكل قبل التنجيد للتأكد من عدم استخدام MDF أو خشب ضعيف في نقاط الضغط.",
        }
    assembly_note = assembly_method or "طريقة التجميع والتجفيف غير موثقة"
    return {
        "agent": "AGENT_09",
        "status": "evaluated",
        "wood_type": wood_type,
        "assembly_method": assembly_note,
        "summary": f"هيكل {wood_type} — {assembly_note}. المتانة الفعلية تعتمد أيضاً على سماكة العوارض والتجفيف والتدعيم.",
    }


def analyze_upholstery_suspension(
    fabric_type: str | None,
    fabric_properties: list[str],
    suspension_type: str | None,
) -> dict:
    """AGENT 10: Analyzes fabric cleanability, stain resistance, and suspension."""
    return {
        "agent": "AGENT_10",
        "fabric": fabric_type or "غير محدد",
        "properties": fabric_properties,
        "suspension": suspension_type or "غير محدد",
        "stain_resistant": any("anti" in p.lower() or "déperlant" in p.lower() or "بقع" in p for p in fabric_properties),
        "summary": f"القماش: {fabric_type or 'غير محدد'} | التعليق: {suspension_type or 'غير محدد'}",
    }


def classify_seller_channel(seller_type: str) -> dict:
    """AGENT 06: Distinguishes direct factory from distributor/broker."""
    labels = {
        "direct_factory": ("مصنع مباشر", True, "إمكانية الشراء المباشر والتفصيل حسب الطلب بأفضل هامش سعري."),
        "artisan_workshop": ("ورشة حرفية", True, "تصنيع محلي مرن حسب المقاسات مع إمكانية معاينة الهيكل قبل التنجيد."),
        "wholesaler": ("تاجر جملة", False, "أسعار تنافسية لكن قد لا تتوفر خدمة التعديل المخصص."),
        "distributor": ("موزع", False, "يتضمن هامش ربح إضافياً مقارنة بالمصنع المباشر."),
        "retailer": ("محل تجزئة", False, "عرض جاهز في المعرض مع تكلفة عرض إضافية."),
        "broker": ("وسيط تجاري", False, "تحقق من السعر الأصلي عند المصنع وموقع المخزن الفعلي."),
    }
    label_ar, is_direct, note = labels.get(seller_type, ("غير مصنف", False, ""))
    return {"agent": "AGENT_06", "label_ar": label_ar, "is_direct_maker": is_direct, "note": note}
