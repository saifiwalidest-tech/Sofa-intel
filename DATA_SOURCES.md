# DATA_SOURCES.md — Source Adapters & Provenance Policy
**Copyright © 2026 saifiwalid**

## 1. سياسة جمع البيانات المشروعة
تلتزم منصة **SOFA INTEL DZ** باحترام شروط استخدام المواقع، قواعد `robots.txt`، حقوق الملكية الفكرية، والقانون الجزائري لحماية الأشخاص الطبيعيين في مجال معالجة المعطيات ذات الطابع الشخصي (القانون 18-07).
- **ممنوع** تجاوز CAPTCHA أو تسجيل الدخول أو أنظمة الحماية التقنية.
- **ممنوع** جمع البيانات الشخصية غير اللازمة (مثل الهواتف الخاصة غير المنشورة تجارياً).

## 2. حالة المصادر (Source Adapter Status)

| Adapter ID | Source Name | Access Method | Status | Notes |
|------------|-------------|---------------|--------|-------|
| `manual_verified` | User-Submitted & Partner Catalog | Direct Form / Partner JSON/CSV | `connected` | نشط بالكامل مع التحقق من الروابط والمصادر |
| `public_web_index` | Global Web Discovery (Google/Bing CSE) | Official Search API (`GOOGLE_CSE_API_KEY`) | `requires_auth` | ينتظر مفتاح Google CSE؛ يعمل بوضع الفهرس المحلي التجريبي عند غيابه |
| `ouedkniss_adapter` | Ouedkniss Public Listings | User-submitted URLs & Authorized Feed | `limited` | يقبل الروابط المقدمة من المستخدمين ولا يتجاوز الحماية الآلية |
| `facebook_adapter` | Facebook Public Pages & Marketplace | Meta Graph API (`FACEBOOK_GRAPH_ACCESS_TOKEN`) | `requires_auth` | يتطلب رمز Graph API مصرحاً به |
| `instagram_adapter` | Instagram Commercial Profiles | Instagram Graph API (`INSTAGRAM_GRAPH_ACCESS_TOKEN`) | `requires_auth` | يتطلب حساب أعمال ورمز وصول مصرحاً به |
| `tiktok_adapter` | TikTok Furniture Makers | TikTok Research/Display API | `requires_auth` | يتطلب اعتماد API رسمي؛ يدعم تحليل النصوص المرفوعة يدوياً |
| `demo_seed` | Synthetic Test Dataset (`is_demo=true`) | Local Seed File | `connected` | **بيانات تجريبية للاختبار فقط** — موسومة بوضوح ولا تُعرض كعروض حقيقية |
