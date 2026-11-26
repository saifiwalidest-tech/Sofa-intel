# SECURITY.md — Cybersecurity & Data Protection Architecture
**Copyright © 2026 saifiwalid**

## الضوابط الأمنية المطبقة
1. **Input Validation & XSS/SQLi Protection:** التحقق الصارم عبر Pydantic v2 وSQLAlchemy Parameterized Queries، وتعقيم النصوص المستخرجة عبر `sanitize_text()`.
2. **SSRF Protection:** فحص الروابط المقدمة من المستخدمين أو المصادر الخارجية لمنع الوصول إلى الشبكات الداخلية (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`, `::1`).
3. **Prompt Injection Protection:** عزل جميع النصوص القادمة من الإعلانات أو الإنترنت باعتبارها بيانات غير موثوقة (`untrusted_external_content`)، وفحصها ضد أنماط حقن التعليمات (`ignore previous instructions`, `system prompt`, إلخ) قبل تمريرها لأي وكيل.
4. **Rate Limiting & RBAC:** محدد معدل الطلبات لكل IP (`API_RATE_LIMIT_PER_MINUTE`) مع دعم أدوار المستخدمين (`consumer`, `verified_seller`, `admin`).
5. **Secrets Management:** جميع المفاتيح في `.env` ولا تُدرج أبداً في الكود أو استجابات الـ API.
6. **Audit Logs:** تسجيل العمليات الحساسة (الإبلاغ، تعديل المصادر، عمليات الإدارة) في جدول `audit_logs`.
