"""Internal Sofa-Type Specialist Agents (AGENT 18 .. AGENT 26).
Evaluates technical requirements specific to each sofa architecture.
Not exposed directly to public frontend UI.
Copyright (c) 2026 saifiwalid.
"""


SPECIALIST_RULES: dict[str, dict] = {
    "straight": {
        "agent_id": "AGENT_18",
        "label_ar": "مختص الأرائك المستقيمة",
        "key_checks": ["توازن الدعم في المنتصف لمنع الهبوط", "عمق المقعد (55-65 سم) للراحة اليومية"],
        "recommended_foam": "D35 / D36",
    },
    "l_shape": {
        "agent_id": "AGENT_19",
        "label_ar": "مختص أرائك الزاوية L",
        "key_checks": ["متانة وصلات ربط الزاوية (معدنية قابلة للفك)", "تطابق كثافة الرغوة بين الشيزلونج والمقاعد"],
        "recommended_foam": "D36 / HR",
    },
    "u_shape": {
        "agent_id": "AGENT_20",
        "label_ar": "مختص الصالونات العائلية U",
        "key_checks": ["توزيع الأحمال على العوارض الطويلة", "سهولة تفكيك الأجزاء للمرور عبر الأبواب والسلالم"],
        "recommended_foam": "D36 / D40",
    },
    "sofa_bed": {
        "agent_id": "AGENT_21",
        "label_ar": "مختص الأرائك القابلة للتحويل إلى سرير",
        "key_checks": ["سماكة وآلية المفصلات الحديدية (Clic-Clac / Rapido)", "مرونة الرغوة لتحمل الطي المتكرر"],
        "recommended_foam": "D35 / HR",
    },
    "modular": {
        "agent_id": "AGENT_22",
        "label_ar": "مختص الصالونات المعيارية Modular",
        "key_checks": ["مشابك تثبيت الوحدات لمنع الانزلاق", "توحيد ارتفاع الأرجل وتناسق القماش"],
        "recommended_foam": "D36 / D40 / HR",
    },
    "turkish": {
        "agent_id": "AGENT_23",
        "label_ar": "مختص الصالونات التركية",
        "key_checks": ["جودة الخياطة والتبطين (Capitonné)", "التحقق من عدم استخدام MDF في القواعد الحاملة"],
        "recommended_foam": "D36 / HR",
    },
    "moroccan": {
        "agent_id": "AGENT_24",
        "label_ar": "مختص الصالونات المغربية والسدادر",
        "key_checks": ["صلابة الحشوة (D36-D45 أو ريبوندد عالي الكثافة)", "متانة الخشب المنحوت وقابلية نزع الأغطية"],
        "recommended_foam": "D40 / D45",
    },
    "italian": {
        "agent_id": "AGENT_25",
        "label_ar": "مختص الصالونات الإيطالية والعصرية",
        "key_checks": ["توازن طبقات الراحة (رغوة + فايبر/ريش)", "نظام تعليق مرن بنوابض Nosag"],
        "recommended_foam": "HR / D40",
    },
    "classic": {
        "agent_id": "AGENT_25",
        "label_ar": "مختص الصالونات الكلاسيكية",
        "key_checks": ["جودة الخشب الصلب المنحوت والتجفيف", "تنجيد متين مقاوم للتآكل"],
        "recommended_foam": "D36 / D40",
    },
    "modern": {
        "agent_id": "AGENT_25",
        "label_ar": "مختص الصالونات العصرية",
        "key_checks": ["جودة القماش المضاد للبقع وسهولة التنظيف", "تشطيب الزوايا والأرجل"],
        "recommended_foam": "D36 / HR",
    },
    "armchair": {
        "agent_id": "AGENT_26",
        "label_ar": "مختص الكراسي الفردية",
        "key_checks": ["زاوية ميلان الظهر ودعم أسفل الظهر", "ثبات القاعدة والأرجل"],
        "recommended_foam": "D35 / HR",
    },
    "recliner": {
        "agent_id": "AGENT_26",
        "label_ar": "مختص الأرائك القابلة للإمالة",
        "key_checks": ["جودة الميكانيزم المعدني وضمانه", "تحمل الأسلاك والمفصلات للوزن"],
        "recommended_foam": "HR / Memory",
    },
}


def analyze_sofa_category_specialist(sofa_type: str, foam_density: str | None, wood_type: str | None) -> dict:
    """Run the category-specific internal engineering specialist."""
    spec = SPECIALIST_RULES.get(sofa_type, SPECIALIST_RULES["modern"])
    checks_str = "؛ ".join(spec["key_checks"])
    foam_match = bool(foam_density and foam_density.upper() in spec["recommended_foam"])
    return {
        "specialist_code": spec["agent_id"],
        "category_label": spec["label_ar"],
        "recommended_foam": spec["recommended_foam"],
        "foam_matches_category": foam_match,
        "technical_note": f"{spec['label_ar']}: يُنصح بالتحقق من {checks_str}. الكثافة الموصى بها لهذه الفئة: {spec['recommended_foam']}.",
    }
