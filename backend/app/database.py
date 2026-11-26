"""SQLAlchemy async database models & session setup.
Copyright (c) 2026 saifiwalid.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from app.config import get_settings

settings = get_settings()
db_url = settings.database_url.replace("+aiosqlite", "")
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
engine = create_engine(db_url, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Seller(Base):
    __tablename__ = "sellers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    seller_type: Mapped[str] = mapped_column(String(50), nullable=False)
    wilaya_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    wilaya_name: Mapped[str] = mapped_column(String(100), nullable=False)
    commune: Mapped[str] = mapped_column(String(120), nullable=False)
    business_address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    public_contact: Mapped[str | None] = mapped_column(String(200), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    has_written_warranty: Mapped[bool] = mapped_column(Boolean, default=False)
    cash_on_delivery: Mapped[bool] = mapped_column(Boolean, default=False)
    provides_invoice: Mapped[bool] = mapped_column(Boolean, default=False)
    custom_orders_supported: Mapped[bool] = mapped_column(Boolean, default=False)
    trust_score: Mapped[float] = mapped_column(Float, default=50.0)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="seller", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    seller_id: Mapped[str] = mapped_column(ForeignKey("sellers.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sofa_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    condition: Mapped[str] = mapped_column(String(30), default="new", index=True)
    images: Mapped[list] = mapped_column(JSON, default=list)
    seats_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dimensions_cm: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Foam
    foam_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    foam_density_claimed: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
    foam_density_documented: Mapped[bool] = mapped_column(Boolean, default=False)
    foam_firmness: Mapped[str | None] = mapped_column(String(40), nullable=True)
    foam_thickness_cm: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Structure
    wood_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    assembly_method: Mapped[str | None] = mapped_column(String(120), nullable=True)
    suspension_type: Mapped[str | None] = mapped_column(String(80), nullable=True)

    # Upholstery
    fabric_type: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    fabric_properties: Mapped[list] = mapped_column(JSON, default=list)
    color: Mapped[str | None] = mapped_column(String(60), nullable=True)

    # Pricing & Delivery
    original_price_dzd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_price_dzd: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    price_status: Mapped[str] = mapped_column(String(40), default="confirmed_dzd")
    warranty_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    delivery_available: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_cost_dzd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cost_dzd: Mapped[int] = mapped_column(Integer, nullable=False)

    # Provenance & Availability
    primary_source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    availability_status: Mapped[str] = mapped_column(String(40), default="available")

    # Scores (never zero-fill missing fields; store min..max range)
    quality_score_min: Mapped[float] = mapped_column(Float, default=0.0)
    quality_score_max: Mapped[float] = mapped_column(Float, default=100.0)
    quality_score_midpoint: Mapped[float] = mapped_column(Float, default=50.0)
    value_for_money_score: Mapped[float] = mapped_column(Float, default=50.0)
    evidence_confidence_score: Mapped[float] = mapped_column(Float, default=50.0)
    data_completeness_score: Mapped[float] = mapped_column(Float, default=50.0)
    comfort_suitability_score: Mapped[float] = mapped_column(Float, default=50.0)
    delivery_cost_score: Mapped[float] = mapped_column(Float, default=50.0)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    seller: Mapped["Seller"] = relationship(back_populates="products")
    provenance_fields: Mapped[list["FieldProvenance"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class FieldProvenance(Base):
    __tablename__ = "field_provenance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(80), nullable=False)
    field_value: Mapped[str | None] = mapped_column(String(300), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(40), nullable=False)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    product: Mapped["Product"] = relationship(back_populates="provenance_fields")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    price_dzd: Mapped[int] = mapped_column(Integer, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="price_history")


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    filters_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AlertRule(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    wilaya_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    max_price_dzd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_foam_density: Mapped[str | None] = mapped_column(String(20), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ListingReport(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reason: Mapped[str] = mapped_column(String(120), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    reporter_contact: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_role: Mapped[str] = mapped_column(String(40), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    target: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    with SessionLocal() as session:
        yield session
