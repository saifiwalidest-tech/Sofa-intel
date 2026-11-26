# ARCHITECTURE.md — SOFA INTEL DZ
**Copyright © 2026 saifiwalid**

## 1. المعمارية العامة (Modular Architecture)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js + TS + Tailwind)               │
│  18 Pages (RTL/LTR, Dark/Light) · Radar Charts · Leaflet/OSM Map        │
│  WebSocket Live Agent Progress · AI Consultant Chat · Comparison Lab    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ REST + WebSocket
┌───────────────────────────────▼─────────────────────────────────────────┐
│                        BACKEND API GATEWAY (FastAPI)                    │
│  Security Middleware (RBAC, Rate Limit, XSS/SQLi/SSRF/Prompt Guard)     │
│  REST Endpoints (/api/v1/*) · WebSocket (/ws/search/{job_id})           │
└───────┬───────────────────────┬─────────────────────────┬───────────────┘
        │                       │                         │
┌───────▼──────────┐   ┌────────▼───────────┐   ┌─────────▼──────────────┐
│ 18-Agent System  │   │  Scoring & Pareto  │   │   Source Adapters      │
│ Agent 00..17     │   │  SQI /100 + Range  │   │  Ouedkniss, FB, IG,    │
│ Orchestrator     │   │  Value / Trust     │   │  TikTok, Web, Manual   │
│ State & Retries  │   │  Pareto Optimizer  │   │  Status + Provenance   │
└───────┬──────────┘   └────────┬───────────┘   └─────────┬──────────────┘
        │                       │                         │
┌───────▼───────────────────────▼─────────────────────────▼───────────────┐
│                         DATA & SEARCH LAYER                             │
│  SQLite (Dev) / PostgreSQL + pgvector + PostGIS (Prod)                  │
│  Field-Level Provenance · Price History · Wilaya/Commune Geo Index      │
│  Multilingual Search (AR / Darja / Latin-Darja / FR / EN)               │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. المبادئ الهندسية الأساسية
1. **Field-Level Provenance:** كل حقل تقني (الكثافة، الخشب، القماش، السعر) يحتفظ بمصدره، تاريخ استخراجه، وتصنيفه (`documented`, `seller_claimed`, `inferred`, `missing`, `conflicting`).
2. **No Fabricated Data:** القيم المفقودة تبقى `null` وتُعرض بوضوح للمستخدم؛ لا تُحوَّل أبداً إلى أصفار في المخططات أو التقييمات.
3. **Graceful Degradation:** عند عدم توفر مفاتيح API خارجية (OpenAI, Meta Graph, TikTok Research)، تعمل المنصة بمحرك التحليل اللغوي والهندسي المحلي الحتمي (`local_heuristic`) وتُظهر حالة كل مصدر بشفافية.
4. **Security by Design:** جميع البيانات الخارجية غير موثوقة وتخضع للتعقيم ومنع Prompt Injection وSSRF.
