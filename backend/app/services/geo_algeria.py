"""Geospatial Intelligence for Algeria (AGENT 07).
Dynamic registry of Algerian wilayas, coordinates, neighbors, and delivery cost estimation.
Copyright (c) 2026 saifiwalid.
"""

import math

WILAYAS: list[dict] = [
    {"code": "01", "name_ar": "أدرار", "name_fr": "Adrar", "lat": 27.8742, "lon": -0.2939, "communes": ["Adrar", "Reggane", "Timimoun"]},
    {"code": "02", "name_ar": "الشلف", "name_fr": "Chlef", "lat": 36.1653, "lon": 1.3345, "communes": ["Chlef", "Ténès", "Oued Fodda"]},
    {"code": "03", "name_ar": "الأغواط", "name_fr": "Laghouat", "lat": 33.8000, "lon": 2.8651, "communes": ["Laghouat", "Aflou", "Ksar El Hirane"]},
    {"code": "04", "name_ar": "أم البواقي", "name_fr": "Oum El Bouaghi", "lat": 35.8754, "lon": 7.1135, "communes": ["Oum El Bouaghi", "Aïn Beïda", "Aïn M'lila"]},
    {"code": "05", "name_ar": "باتنة", "name_fr": "Batna", "lat": 35.5560, "lon": 6.1741, "communes": ["Batna", "Barika", "Aïn Touta"]},
    {"code": "06", "name_ar": "بجاية", "name_fr": "Béjaïa", "lat": 36.7509, "lon": 5.0567, "communes": ["Béjaïa", "Akbou", "El Kseur"]},
    {"code": "07", "name_ar": "بسكرة", "name_fr": "Biskra", "lat": 34.8504, "lon": 5.7281, "communes": ["Biskra", "Tolga", "Sidi Okba"]},
    {"code": "08", "name_ar": "بشار", "name_fr": "Béchar", "lat": 31.6167, "lon": -2.2167, "communes": ["Béchar", "Kenadsa", "Abadla"]},
    {"code": "09", "name_ar": "البليدة", "name_fr": "Blida", "lat": 36.4700, "lon": 2.8277, "communes": ["Blida", "Boufarik", "Ouled Yaïch", "Larbaa"]},
    {"code": "10", "name_ar": "البويرة", "name_fr": "Bouira", "lat": 36.3749, "lon": 3.9020, "communes": ["Bouira", "Lakhdaria", "Sour El Ghozlane"]},
    {"code": "11", "name_ar": "تمنراست", "name_fr": "Tamanrasset", "lat": 22.7850, "lon": 5.5228, "communes": ["Tamanrasset", "In Salah"]},
    {"code": "12", "name_ar": "تبسة", "name_fr": "Tébessa", "lat": 35.4042, "lon": 8.1242, "communes": ["Tébessa", "Bir El Ater", "Chéria"]},
    {"code": "13", "name_ar": "تلمسان", "name_fr": "Tlemcen", "lat": 34.8783, "lon": -1.3150, "communes": ["Tlemcen", "Maghnia", "Mansourah"]},
    {"code": "14", "name_ar": "تيارت", "name_fr": "Tiaret", "lat": 35.3710, "lon": 1.3170, "communes": ["Tiaret", "Frenda", "Sougueur"]},
    {"code": "15", "name_ar": "تيزي وزو", "name_fr": "Tizi Ouzou", "lat": 36.7118, "lon": 4.0459, "communes": ["Tizi Ouzou", "Azazga", "Draâ Ben Khedda"]},
    {"code": "16", "name_ar": "الجزائر", "name_fr": "Alger", "lat": 36.7538, "lon": 3.0588, "communes": ["Alger Centre", "Bab Ezzouar", "Chéraga", "Birkhadem", "Rouiba", "Draria"]},
    {"code": "17", "name_ar": "الجلفة", "name_fr": "Djelfa", "lat": 34.6728, "lon": 3.2630, "communes": ["Djelfa", "Aïn Oussera", "Messaad"]},
    {"code": "18", "name_ar": "جيجل", "name_fr": "Jijel", "lat": 36.8205, "lon": 5.7667, "communes": ["Jijel", "Taher", "El Milia"]},
    {"code": "19", "name_ar": "سطيف", "name_fr": "Sétif", "lat": 36.1911, "lon": 5.4137, "communes": ["Sétif", "El Eulma", "Aïn Oulmene"]},
    {"code": "20", "name_ar": "سعيدة", "name_fr": "Saïda", "lat": 34.8303, "lon": 0.1517, "communes": ["Saïda", "Aïn El Hadjar"]},
    {"code": "21", "name_ar": "سكيكدة", "name_fr": "Skikda", "lat": 36.8762, "lon": 6.9092, "communes": ["Skikda", "Azzaba", "Collo"]},
    {"code": "22", "name_ar": "سيدي بلعباس", "name_fr": "Sidi Bel Abbès", "lat": 35.1899, "lon": -0.6309, "communes": ["Sidi Bel Abbès", "Télagh"]},
    {"code": "23", "name_ar": "عنابة", "name_fr": "Annaba", "lat": 36.9000, "lon": 7.7667, "communes": ["Annaba", "El Bouni", "Berrahal"]},
    {"code": "24", "name_ar": "قالمة", "name_fr": "Guelma", "lat": 36.4621, "lon": 7.4261, "communes": ["Guelma", "Oued Zenati"]},
    {"code": "25", "name_ar": "قسنطينة", "name_fr": "Constantine", "lat": 36.3650, "lon": 6.6147, "communes": ["Constantine", "El Khroub", "Ali Mendjeli"]},
    {"code": "26", "name_ar": "المدية", "name_fr": "Médéa", "lat": 36.2642, "lon": 2.7539, "communes": ["Médéa", "Berrouaghia", "Ksar El Boukhari"]},
    {"code": "27", "name_ar": "مستغانم", "name_fr": "Mostaganem", "lat": 35.9312, "lon": 0.0892, "communes": ["Mostaganem", "Aïn Tédelès"]},
    {"code": "28", "name_ar": "المسيلة", "name_fr": "M'Sila", "lat": 35.7058, "lon": 4.5419, "communes": ["M'Sila", "Bou Saâda", "Sidi Aïssa"]},
    {"code": "29", "name_ar": "معسكر", "name_fr": "Mascara", "lat": 35.3966, "lon": 0.1403, "communes": ["Mascara", "Sig", "Mohammadia"]},
    {"code": "30", "name_ar": "ورقلة", "name_fr": "Ouargla", "lat": 31.9493, "lon": 5.3250, "communes": ["Ouargla", "Hassi Messaoud"]},
    {"code": "31", "name_ar": "وهران", "name_fr": "Oran", "lat": 35.6969, "lon": -0.6331, "communes": ["Oran", "Bir El Djir", "Es Sénia", "Arzew"]},
    {"code": "32", "name_ar": "البيض", "name_fr": "El Bayadh", "lat": 33.6832, "lon": 1.0193, "communes": ["El Bayadh", "Bougtob"]},
    {"code": "33", "name_ar": "إليزي", "name_fr": "Illizi", "lat": 26.4833, "lon": 8.4667, "communes": ["Illizi", "Djanet"]},
    {"code": "34", "name_ar": "برج بوعريريج", "name_fr": "Bordj Bou Arréridj", "lat": 36.0732, "lon": 4.7611, "communes": ["Bordj Bou Arréridj", "Ras El Oued"]},
    {"code": "35", "name_ar": "بومرداس", "name_fr": "Boumerdès", "lat": 36.7664, "lon": 3.4772, "communes": ["Boumerdès", "Boudouaou", "Khemis El Khechna"]},
    {"code": "36", "name_ar": "الطارف", "name_fr": "El Tarf", "lat": 36.7672, "lon": 8.3138, "communes": ["El Tarf", "El Kala"]},
    {"code": "37", "name_ar": "تندوف", "name_fr": "Tindouf", "lat": 27.6711, "lon": -8.1474, "communes": ["Tindouf"]},
    {"code": "38", "name_ar": "تيسمسيلت", "name_fr": "Tissemsilt", "lat": 35.6072, "lon": 1.8108, "communes": ["Tissemsilt", "Theniet El Had"]},
    {"code": "39", "name_ar": "الوادي", "name_fr": "El Oued", "lat": 33.3561, "lon": 6.8632, "communes": ["El Oued", "Guemar"]},
    {"code": "40", "name_ar": "خنشلة", "name_fr": "Khenchela", "lat": 35.4358, "lon": 7.1433, "communes": ["Khenchela", "Kais"]},
    {"code": "41", "name_ar": "سوق أهراس", "name_fr": "Souk Ahras", "lat": 36.2864, "lon": 7.9511, "communes": ["Souk Ahras", "Sedrata"]},
    {"code": "42", "name_ar": "تيبازة", "name_fr": "Tipaza", "lat": 36.5897, "lon": 2.4475, "communes": ["Tipaza", "Koléa", "Cherchell"]},
    {"code": "43", "name_ar": "ميلة", "name_fr": "Mila", "lat": 36.4503, "lon": 6.2644, "communes": ["Mila", "Chelghoum Laïd"]},
    {"code": "44", "name_ar": "عين الدفلى", "name_fr": "Aïn Defla", "lat": 36.2640, "lon": 1.9679, "communes": ["Aïn Defla", "Khemis Miliana"]},
    {"code": "45", "name_ar": "النعامة", "name_fr": "Naâma", "lat": 33.2667, "lon": -0.3167, "communes": ["Naâma", "Mécheria"]},
    {"code": "46", "name_ar": "عين تموشنت", "name_fr": "Aïn Témouchent", "lat": 35.2975, "lon": -1.1404, "communes": ["Aïn Témouchent", "Beni Saf"]},
    {"code": "47", "name_ar": "غرداية", "name_fr": "Ghardaïa", "lat": 32.4909, "lon": 3.6735, "communes": ["Ghardaïa", "Berriane"]},
    {"code": "48", "name_ar": "غليزان", "name_fr": "Relizane", "lat": 35.7373, "lon": 0.5560, "communes": ["Relizane", "Oued Rhiou"]},
    {"code": "49", "name_ar": "تيميمون", "name_fr": "Timimoun", "lat": 29.2639, "lon": 0.2309, "communes": ["Timimoun"]},
    {"code": "50", "name_ar": "برج باجي مختار", "name_fr": "Bordj Badji Mokhtar", "lat": 21.3275, "lon": 0.9553, "communes": ["Bordj Badji Mokhtar"]},
    {"code": "51", "name_ar": "أولاد جلال", "name_fr": "Ouled Djellal", "lat": 34.4333, "lon": 5.0667, "communes": ["Ouled Djellal"]},
    {"code": "52", "name_ar": "بني عباس", "name_fr": "Béni Abbès", "lat": 30.1322, "lon": -2.1667, "communes": ["Béni Abbès"]},
    {"code": "53", "name_ar": "عين صالح", "name_fr": "In Salah", "lat": 27.1936, "lon": 2.4608, "communes": ["In Salah"]},
    {"code": "54", "name_ar": "عين قزام", "name_fr": "In Guezzam", "lat": 19.5722, "lon": 5.7722, "communes": ["In Guezzam"]},
    {"code": "55", "name_ar": "تقرت", "name_fr": "Touggourt", "lat": 33.1053, "lon": 6.0580, "communes": ["Touggourt"]},
    {"code": "56", "name_ar": "جانت", "name_fr": "Djanet", "lat": 24.5542, "lon": 9.4844, "communes": ["Djanet"]},
    {"code": "57", "name_ar": "المغير", "name_fr": "El M'Ghair", "lat": 33.9500, "lon": 5.9242, "communes": ["El M'Ghair"]},
    {"code": "58", "name_ar": "المنيعة", "name_fr": "El Meniaa", "lat": 30.5792, "lon": 2.8792, "communes": ["El Meniaa"]},
]

WILAYA_BY_CODE = {w["code"]: w for w in WILAYAS}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


def estimate_delivery_dzd(from_code: str, to_code: str) -> tuple[int, float]:
    """Estimate furniture truck delivery cost in DZD and distance in km."""
    w1 = WILAYA_BY_CODE.get(from_code)
    w2 = WILAYA_BY_CODE.get(to_code)
    if not w1 or not w2:
        return 6000, 0.0
    if from_code == to_code:
        return 2500, 15.0
    dist = haversine_km(w1["lat"], w1["lon"], w2["lat"], w2["lon"])
    estimated = int(round((3000 + dist * 45) / 500.0) * 500)
    return min(max(estimated, 3000), 35000), dist


def resolve_wilaya_from_text(text: str) -> dict | None:
    lowered = text.lower()
    for w in WILAYAS:
        stem_ar = w["name_ar"][2:] if w["name_ar"].startswith("ال") else w["name_ar"]
        if w["name_ar"] in text or (len(stem_ar) >= 3 and stem_ar in text) or w["name_fr"].lower() in lowered or w["code"] == lowered.strip():
            return w
    return None
