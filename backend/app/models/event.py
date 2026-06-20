from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, Numeric, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..database import Base, UUID


class EventStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TicketType(str, enum.Enum):
    GENERAL = "general"
    VIP = "vip"
    SPONSOR = "sponsor"
    COMPLIMENTARY = "complimentary"


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    
    date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(500), nullable=False)
    
    capacity = Column(Integer, nullable=True)
    
    is_ticketed = Column(Boolean, default=False)
    ticket_price = Column(Numeric(precision=10, scale=2), nullable=True)
    has_sponsorship = Column(Boolean, default=False)
    
    status = Column(SQLEnum(EventStatus), nullable=False, default=EventStatus.UPCOMING)
    
    # Flexible form configuration for registration
    registration_form_config = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(UUID, ForeignKey("events.id"), nullable=False)
    constituent_id = Column(UUID, ForeignKey("constituents.id"), nullable=False)
    
    ticket_type = Column(SQLEnum(TicketType), nullable=False, default=TicketType.GENERAL)
    
    # QR code for check-in
    qr_code = Column(String(255), unique=True, nullable=False)
    
    checked_in_at = Column(DateTime(timezone=True), nullable=True)
    
    amount_paid = Column(Numeric(precision=10, scale=2), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
