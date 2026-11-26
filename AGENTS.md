# AGENTS.md — 18-Agent Multi-Agent System Specification
**Copyright © 2026 saifiwalid**

| ID | Agent Name | Role & Core Responsibilities | Implementation Module |
|----|------------|------------------------------|-----------------------|
| **AGENT 00** | Master Orchestrator | Task decomposition, parallel execution, deduplication, conflict resolution, retries, loop prevention | `backend/app/agents/orchestrator.py` |
| **AGENT 01** | Global Web Discovery | Multilingual semantic & keyword discovery across Algerian web stores & directories | `backend/app/agents/discovery.py` |
| **AGENT 02** | Ouedkniss Intelligence | Authorized Ouedkniss listing extraction, price tracking, duplicate detection | `backend/app/agents/discovery.py` |
| **AGENT 03** | Facebook Intelligence | Authorized public pages/groups commercial analysis without bypassing auth | `backend/app/agents/discovery.py` |
| **AGENT 04** | Instagram Intelligence | Authorized public showroom/manufacturer post & visual extraction | `backend/app/agents/discovery.py` |
| **AGENT 05** | TikTok Video Intelligence | Video metadata, OCR/STT transcript analysis for prices & material claims | `backend/app/agents/discovery.py` |
| **AGENT 06** | Local Manufacturer Hunter | Classifies Direct Factory vs Workshop vs Wholesaler vs Distributor vs Retailer vs Broker | `backend/app/agents/domain_experts.py` |
| **AGENT 07** | Geospatial Intelligence | Dynamic Algerian wilaya/commune registry, distance calculation, delivery cost estimation | `backend/app/agents/geospatial.py` |
| **AGENT 08** | Foam Engineering Expert | Analyzes D20–D50, HR, Memory, Rebonded; distinguishes documented vs claimed density | `backend/app/agents/domain_experts.py` |
| **AGENT 09** | Wood Engineering Expert | Evaluates Hêtre, Chêne, Pin, Sapin, Massif, Contreplaqué, MDF, OSB, Aggloméré, Metal | `backend/app/agents/domain_experts.py` |
| **AGENT 10** | Upholstery & Suspension Expert | Evaluates Velours, Bouclé, Chenille, Lin, Microfibre, Cuir, Martindale, Springs/Webbing | `backend/app/agents/domain_experts.py` |
| **AGENT 11** | Computer Vision Analyst | Classifies sofa type, seat count, colors, duplicate images; forbids inferring internal foam/wood | `backend/app/agents/vision_pricing.py` |
| **AGENT 12** | Pricing Intelligence | DZD vs Centime normalization, median/fair price range, outlier detection, price/seat | `backend/app/agents/vision_pricing.py` |
| **AGENT 13** | Quality & Value Optimizer | Multi-objective & Pareto Front optimization across price, materials, delivery, confidence | `backend/app/agents/optimizer_trust.py` |
| **AGENT 14** | Seller Trust & Fraud Detection | Risk indicators (duplicate photos, missing address, conflicting specs) without baseless accusations | `backend/app/agents/optimizer_trust.py` |
| **AGENT 15** | Data Verification & Fact Checking | Tags every field: `documented`, `seller_claimed`, `inferred`, `missing`, `conflicting` | `backend/app/agents/verification_monitor.py` |
| **AGENT 16** | Market Monitoring | Periodic offer refresh, price drops, expired listings, alert triggers, trend reports | `backend/app/agents/verification_monitor.py` |
| **AGENT 17** | AI Shopping Consultant | Natural language parser (AR / Darja / FR / EN) converting user intent to structured queries | `backend/app/agents/consultant.py` |
