# DEPLOYMENT.md — Local & Production Deployment Guide
**Copyright © 2026 saifiwalid**

## 1. بيئة التطوير المحلية (بدون Docker)
- **Backend**: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
- **Frontend**: `cd frontend && npm install && npm run dev`

## 2. بيئة الإنتاج (Docker Compose + PostgreSQL/PostGIS + Redis + Meilisearch)
```bash
cp .env.example .env
# عدّل كلمات المرور ومفاتيح API المصرح بها في .env
docker compose up -d --build
```

## 3. القيود التقنية والتكاليف
- **بدون مفاتيح مدفوعة:** تعمل المنصة بالكامل بالمحرك المحلي الحتمي (`LLM_PROVIDER=local_heuristic`) بتكلفة 0 دج.
- **المصادر الخارجية المقيدة:** Ouedkniss وFacebook وInstagram وTikTok لا يتم تجاوز أنظمتها؛ عند غياب مفاتيح API رسمية تعتمد المنصة على الروابط المقدمة من المستخدمين والشراكات التجارية.
