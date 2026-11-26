"""Pydantic v2 schemas for SOFA INTEL DZ API. Copyright (c) 2026 saifiwalid."""

from datetime import datetime
from pydantic import BaseModel, Field


class CustomWeights(BaseModel):
    foam: float = Field(default=25.0, ge=0, le=100)
    structure: float = Field(default=25.0, ge=0, le=100)
    upholstery: float = Field(default=15.0, ge=0, le=100)
    suspension: float = Field(default=15.0, ge=0, le=100)
    craftsmanship: float = Field(default=10.0, ge=0, le=100)
    warranty: float = Field(default=10.0, ge=0, le=100)


class SellerOut(BaseModel):
    id: str
    name: str
    seller_type: str
    wilaya_code: str
    wilaya_name: str
    commune: str
    business_address: str | None
    public_contact: str | None
    latitude: float | None
    longitude: float | None
    has_written_warranty: bool
    cash_on_delivery: bool
    provides_invoice: bool
    custom_orders_supported: bool
    trust_score: float
    is_demo: bool

    class Config:
        orm_mode = True


class ProvenanceOut(BaseModel):
    field_name: str
    field_value: str | None
    verification_status: str
    source_name: str
    source_url: str | None
    confidence: float
    extracted_at: datetime

    class Config:
        orm_mode = True


class PriceHistoryOut(BaseModel):
    price_dzd: int
    recorded_at: datetime
    source_name: str

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: str
    title: str
    description: str | None
    sofa_type: str
    condition: str
    images: list[str]
    seats_count: int | None
    dimensions_cm: str | None
    foam_type: str | None
    foam_density_claimed: str | None
    foam_density_documented: bool
    foam_firmness: str | None
    foam_thickness_cm: float | None
    wood_type: str | None
    assembly_method: str | None
    suspension_type: str | None
    fabric_type: str | None
    fabric_properties: list[str]
    color: str | None
    original_price_dzd: int | None
    current_price_dzd: int
    price_status: str
    warranty_months: int | None
    delivery_available: bool
    delivery_cost_dzd: int | None
    total_cost_dzd: int
    primary_source_name: str
    source_url: str
    published_at: datetime
    last_verified_at: datetime
    availability_status: str
    quality_score_min: float
    quality_score_max: float
    quality_score_midpoint: float
    value_for_money_score: float
    evidence_confidence_score: float
    data_completeness_score: float
    comfort_suitability_score: float
    delivery_cost_score: float
    is_demo: bool
    seller: SellerOut
    provenance_fields: list[ProvenanceOut] = []
    price_history: list[PriceHistoryOut] = []

    class Config:
        orm_mode = True


class CompareRequest(BaseModel):
    product_ids: list[str] = Field(..., min_items=2, max_items=6)


class ConsultantRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=1500)
    user_wilaya_code: str | None = None


class VerificationChecklistRequest(BaseModel):
    product_id: str | None = None
    language: str = Field(default="ar", regex="^(ar|darja|fr)$")
    foam_density: str | None = None
    wood_type: str | None = None


class VisualSearchRequest(BaseModel):
    sofa_type: str | None = None
    color: str | None = None
    seats_count: int | None = None
    image_filename: str | None = None


class ProductSubmitRequest(BaseModel):
    title: str = Field(..., min_length=4, max_length=300)
    sofa_type: str = "l_shape"
    current_price_dzd: int = Field(..., gt=1000)
    wilaya_code: str = "09"
    commune: str = "Blida"
    seller_name: str = Field(..., min_length=2, max_length=200)
    seller_type: str = "direct_factory"
    source_url: str = Field(..., min_length=8, max_length=500)
    foam_density_claimed: str | None = None
    wood_type: str | None = None
    fabric_type: str | None = None
    suspension_type: str | None = None
    warranty_months: int | None = None


class SavedSearchRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    filters_json: dict = Field(default_factory=dict)


class AlertRequest(BaseModel):
    label: str = Field(..., min_length=3, max_length=200)
    wilaya_code: str | None = None
    max_price_dzd: int | None = None
    min_foam_density: str | None = None


class ReportRequest(BaseModel):
    product_id: str | None = None
    reason: str = Field(..., min_length=3, max_length=120)
    details: str = Field(..., min_length=5, max_length=2000)
    reporter_contact: str | None = None
