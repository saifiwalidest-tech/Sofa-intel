# DATABASE_SCHEMA.md — Smart Database Schema
**Copyright © 2026 saifiwalid**

## الجداول الرئيسية (Core Tables)

### 1. `sellers`
- `id` (String UUID, PK)
- `name`, `seller_type` (`direct_factory`, `artisan_workshop`, `wholesaler`, `distributor`, `retailer`, `broker`)
- `wilaya_code`, `wilaya_name`, `commune`, `business_address`, `public_contact`
- `latitude`, `longitude`
- `has_written_warranty`, `cash_on_delivery`, `provides_invoice`, `custom_orders_supported`
- `trust_score` (Float 0..100), `is_demo` (Boolean)

### 2. `products`
- `id` (String UUID, PK), `seller_id` (FK -> `sellers.id`)
- `title`, `sofa_type` (14 categories: `straight`, `l_shape`, `u_shape`, `sofa_bed`, `modular`, `turkish`, `moroccan`, `italian`, `classic`, `modern`, `armchair`, `recliner`, `used`, `custom_made`)
- `condition` (`new`, `used`, `custom`), `images` (JSON array), `seats_count`, `dimensions_cm`
- **Foam**: `foam_type`, `foam_density_claimed`, `foam_density_documented`, `foam_firmness`, `foam_thickness_cm`
- **Structure**: `wood_type`, `assembly_method`, `suspension_type`
- **Upholstery**: `fabric_type`, `fabric_properties` (JSON), `color`
- **Pricing & Delivery**: `original_price_dzd`, `current_price_dzd`, `price_status`, `warranty_months`, `delivery_available`, `delivery_cost_dzd`, `total_cost_dzd`
- **Provenance & Status**: `primary_source_name`, `source_url`, `published_at`, `last_verified_at`, `availability_status`
- **Scores**: `quality_score_min`, `quality_score_max`, `quality_score_midpoint`, `value_for_money_score`, `evidence_confidence_score`, `data_completeness_score`, `comfort_suitability_score`, `delivery_cost_score`
- `is_demo` (Boolean — strictly tagged)

### 3. `field_provenance`
- `id`, `product_id` (FK), `field_name`, `field_value`, `verification_status` (`documented`, `seller_claimed`, `inferred`, `missing`, `conflicting`), `source_name`, `source_url`, `confidence` (0..1), `extracted_at`

### 4. `price_history`
- `id`, `product_id` (FK), `price_dzd`, `recorded_at`, `source_name`

### 5. `saved_searches`, `alerts`, `reports`, `audit_logs`
- حفظ الفلاتر، تنبيهات الأسعار، بلاغات الإعلانات غير الصحيحة، وسجل التدقيق الأمني.
