from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from ..models.event import EventStatus, TicketType


class EventBase(BaseModel):
    name: str
    date: datetime
    location: str
    capacity: Optional[int] = Field(None, gt=0)
    is_ticketed: bool = False
    ticket_price: Optional[Decimal] = Field(None, ge=0)
    has_sponsorship: bool = False
    status: EventStatus = EventStatus.UPCOMING
    registration_form_config: Optional[Dict[str, Any]] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_ticketed: Optional[bool] = None
    ticket_price: Optional[Decimal] = Field(None, ge=0)
    has_sponsorship: Optional[bool] = None
    status: Optional[EventStatus] = None
    registration_form_config: Optional[Dict[str, Any]] = None


class EventResponse(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    event_id: UUID
    constituent_id: UUID
    ticket_type: TicketType = TicketType.GENERAL
    amount_paid: Optional[Decimal] = Field(None, ge=0)


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: UUID
    qr_code: str
    checked_in_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
