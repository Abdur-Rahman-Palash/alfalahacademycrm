from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, Numeric, ForeignKey, Integer, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..database import Base, UUID, ARRAY


class DonationType(str, enum.Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    PLEDGE = "pledge"
    IN_KIND = "in_kind"
    MATCHING = "matching"
    SOFT_CREDIT = "soft_credit"


class PaymentMethod(str, enum.Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    SQUARE = "square"
    ZELLE = "zelle"
    CHECK = "check"
    CASH = "cash"


class DonationStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Donation(Base):
    __tablename__ = "donations"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituent_id = Column(UUID, ForeignKey("constituents.id"), nullable=False)
    
    # Monetary value - NEVER use float for money
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    
    type = Column(SQLEnum(DonationType), nullable=False, default=DonationType.ONE_TIME)
    campaign_id = Column(UUID, ForeignKey("campaigns.id"), nullable=True)
    event_id = Column(UUID, ForeignKey("events.id"), nullable=True)
    
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    
    status = Column(SQLEnum(DonationStatus), nullable=False, default=DonationStatus.PENDING)
    
    # Soft credit
    soft_credit_for = Column(UUID, ForeignKey("constituents.id"), nullable=True)
    is_anonymous = Column(Boolean, default=False)
    
    # Hijri date stored alongside Gregorian
    hijri_date = Column(String(50), nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RecurringFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    HIJRI_CUSTOM = "hijri_custom"


class RecurringStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class RecurringSchedule(Base):
    __tablename__ = "recurring_schedules"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituent_id = Column(UUID, ForeignKey("constituents.id"), nullable=False)
    
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    frequency = Column(SQLEnum(RecurringFrequency), nullable=False, default=RecurringFrequency.MONTHLY)
    
    # Hijri months for custom Islamic schedules (e.g., [9] for Ramadan, [12] for Dhul Hijjah)
    hijri_months = Column(ARRAY(Integer), nullable=True)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    
    stripe_subscription_id = Column(String(255), nullable=True)
    status = Column(SQLEnum(RecurringStatus), nullable=False, default=RecurringStatus.ACTIVE)
    
    next_charge_date = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
