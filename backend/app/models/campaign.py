from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, Numeric, Date
from sqlalchemy.sql import func
import uuid
import enum

from ..database import Base, UUID


class CampaignType(str, enum.Enum):
    GENERAL = "general"
    RAMADAN = "ramadan"
    DHUL_HIJJAH = "dhul_hijjah"
    ANNUAL = "annual"
    EVENT = "event"
    GASSO = "gasso"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    
    type = Column(SQLEnum(CampaignType), nullable=False, default=CampaignType.GENERAL)
    
    # Monetary goal
    goal_amount = Column(Numeric(precision=12, scale=2), nullable=True)
    
    # Date range
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Hijri dates for Islamic campaigns
    hijri_start = Column(String(50), nullable=True)
    hijri_end = Column(String(50), nullable=True)
    
    is_islamic_calendar = Column(Boolean, default=False)
    
    status = Column(SQLEnum(CampaignStatus), nullable=False, default=CampaignStatus.DRAFT)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
