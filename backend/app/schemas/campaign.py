from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from ..models.campaign import CampaignType, CampaignStatus


class CampaignBase(BaseModel):
    name: str
    type: CampaignType = CampaignType.GENERAL
    goal_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: date
    end_date: date
    hijri_start: Optional[str] = None
    hijri_end: Optional[str] = None
    is_islamic_calendar: bool = False
    status: CampaignStatus = CampaignStatus.DRAFT


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CampaignType] = None
    goal_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    hijri_start: Optional[str] = None
    hijri_end: Optional[str] = None
    is_islamic_calendar: Optional[bool] = None
    status: Optional[CampaignStatus] = None


class CampaignResponse(CampaignBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
