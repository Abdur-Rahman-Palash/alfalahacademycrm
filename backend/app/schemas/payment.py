from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DonorInfo(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None


class DedicationInfo(BaseModel):
    type: str
    name: str
    email: Optional[str] = None


class PaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in cents")
    currency: str = Field(default="usd")
    frequency: str = Field(default="one_time")
    donor: DonorInfo
    dedication: Optional[DedicationInfo] = None
    campaignId: Optional[str] = None
    isAnonymous: bool = False


class PaymentIntentResponse(BaseModel):
    clientSecret: str
    paymentIntentId: str
    amount: float


class SubscriptionRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in cents")
    currency: str = Field(default="usd")
    frequency: str = Field(default="month")
    donor: DonorInfo
    campaignId: Optional[str] = None
    isAnonymous: bool = False


class SubscriptionResponse(BaseModel):
    subscriptionId: str
    clientSecret: str
    amount: float
    frequency: str


class DonationResponse(BaseModel):
    id: str
    donor_id: str
    amount: float
    currency: str
    payment_status: str
    donation_type: str
    payment_date: datetime
    frequency: Optional[str] = None
    campaign_id: Optional[str] = None
    is_anonymous: bool = False
    
    class Config:
        from_attributes = True


class RecurringScheduleResponse(BaseModel):
    id: str
    donor_id: str
    amount: float
    frequency: str
    start_date: datetime
    status: str
    campaign_id: Optional[str] = None
    next_payment_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
