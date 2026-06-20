from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from ..models.donation import DonationType, PaymentMethod, DonationStatus, RecurringFrequency, RecurringStatus


class DonationBase(BaseModel):
    constituent_id: UUID
    amount: Decimal = Field(..., ge=0)
    type: DonationType = DonationType.ONE_TIME
    campaign_id: Optional[UUID] = None
    event_id: Optional[UUID] = None
    payment_method: PaymentMethod
    stripe_payment_intent_id: Optional[str] = None
    status: DonationStatus = DonationStatus.PENDING
    soft_credit_for: Optional[UUID] = None
    is_anonymous: bool = False
    hijri_date: Optional[str] = None
    notes: Optional[str] = None


class DonationCreate(DonationBase):
    pass


class DonationUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, ge=0)
    type: Optional[DonationType] = None
    campaign_id: Optional[UUID] = None
    event_id: Optional[UUID] = None
    payment_method: Optional[PaymentMethod] = None
    stripe_payment_intent_id: Optional[str] = None
    status: Optional[DonationStatus] = None
    soft_credit_for: Optional[UUID] = None
    is_anonymous: Optional[bool] = None
    hijri_date: Optional[str] = None
    notes: Optional[str] = None


class DonationResponse(DonationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RecurringScheduleBase(BaseModel):
    constituent_id: UUID
    amount: Decimal = Field(..., ge=0)
    frequency: RecurringFrequency = RecurringFrequency.MONTHLY
    hijri_months: Optional[list[int]] = None
    start_date: date
    end_date: Optional[date] = None
    stripe_subscription_id: Optional[str] = None
    status: RecurringStatus = RecurringStatus.ACTIVE
    next_charge_date: Optional[date] = None


class RecurringScheduleCreate(RecurringScheduleBase):
    pass


class RecurringScheduleUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, ge=0)
    frequency: Optional[RecurringFrequency] = None
    hijri_months: Optional[list[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    stripe_subscription_id: Optional[str] = None
    status: Optional[RecurringStatus] = None
    next_charge_date: Optional[date] = None


class RecurringScheduleResponse(RecurringScheduleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
