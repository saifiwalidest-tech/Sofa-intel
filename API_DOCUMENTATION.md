# API_DOCUMENTATION.md — REST & WebSocket Reference
**Copyright © 2026 saifiwalid**

Base URL: `http://127.0.0.1:8000` (Swagger UI: `/docs`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | فحص صحة الخادم وقاعدة البيانات |
| `GET` | `/api/v1/products` | بحث وتصفية شاملة (19+ فلتر، لغات متعددة، ترقيم الصفحات) |
| `GET` | `/api/v1/products/{id}` | تفاصيل المنتج مع `field_provenance` وسجل الأسعار |
| `POST` | `/api/v1/products/submit` | إدخال إعلان أو رابط مصدر للتحليل والتحقق |
| `POST` | `/api/v1/compare` | مقارنة حتى 6 منتجات + تحليل الفروقات والأسئلة الحرجة |
| `POST` | `/api/v1/scoring/custom` | إعادة حساب التقييم بأوزان المستخدم المخصصة |
| `GET` | `/api/v1/optimize/pareto` | استخراج التوليفات المثلى ونتائج Pareto Front |
| `POST` | `/api/v1/consultant/ask` | مستشار الشراء الذكي (AR / Darja / FR / EN) |
| `POST` | `/api/v1/verification-lab/checklist` | توليد قائمة فحص ورسالة تواصل جاهزة للبائع |
| `POST` | `/api/v1/visual-search` | البحث عن أرائك مشابهة انطلاقاً من وصف/لون/صورة مرفوعة |
| `GET` | `/api/v1/geo/wilayas` | التقسيم الإداري للجزائر + إحصاءات العروض |
| `GET` | `/api/v1/manufacturers` | دليل المصانع والورشات والحرفيين |
| `GET` | `/api/v1/price-observatory` | مرصد الأسعار والوسيط السعري والنطاق العادل |
| `GET` | `/api/v1/adapters/status` | حالة جميع Source Adapters ومواعيد المزامنة |
| `GET` | `/api/v1/agents/status` | حالة الـ 18 وكيلاً ومهامهم |
| `POST` | `/api/v1/saved-searches` | حفظ بحث دائم |
| `GET/POST` | `/api/v1/alerts` | إدارة التنبيهات الذكية |
| `POST` | `/api/v1/reports` | الإبلاغ عن إعلان غير صحيح |
| `WS` | `/ws/search/{job_id}` | بث مباشر لتقدم الوكلاء أثناء البحث |
