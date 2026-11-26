# TEST_REPORT.md — Quality Assurance & Test Coverage
**Copyright © 2026 saifiwalid**

## نطاق الاختبارات المنفذة (`backend/tests/`)
1. **Unit Tests — Scoring & Missing Data (`test_scoring.py`):**
   - التحقق من عدم منح أصفار للحقول المفقودة وحساب النطاق المحتمل (`min..max`).
   - التحقق من تمييز الرغوة الموثقة بشهادة عن الادعاء التسويقي فقط.
   - التحقق من تطبيع الأسعار بين الدينار الجزائري والسنتيم (`12 مليون سنتيم = 120,000 DZD`).
2. **Unit Tests — Multi-Agent & Consultant (`test_agents.py`):**
   - اختبار Agent 17 مع جمل بالدارجة الجزائرية والفرنسية والعربية.
   - اختبار Agent 13 (Pareto Front) وAgent 15 (Fact Checking).
3. **Security Tests (`test_security.py`):**
   - اختبار صد محاولات Prompt Injection في نصوص الإعلانات.
   - اختبار صد روابط SSRF الداخلية (`http://127.0.0.1`, `http://169.254.169.254`).
   - اختبار تعقيم XSS.
4. **API Integration Tests (`test_api.py`):**
   - اختبار جميع المسارات الرئيسية (`/health`, `/api/v1/products`, `/api/v1/compare`, `/api/v1/consultant/ask`, `/api/v1/optimize/pareto`, `/api/v1/adapters/status`).
