from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from ..models.scholarship import GassoStatus


class GassoRecordBase(BaseModel):
    student_id: UUID
    constituent_id: UUID
    academic_year: str
    pledge_amount: Decimal = Field(..., ge=0)
    approved_amount: Optional[Decimal] = Field(None, ge=0)
    funded_amount: Decimal = Field(default=0, ge=0)
    status: GassoStatus = GassoStatus.PLEDGED
    soft_credit_applied: bool = False
    stage_history: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class GassoRecordCreate(GassoRecordBase):
    pass


class GassoRecordUpdate(BaseModel):
    student_id: Optional[UUID] = None
    constituent_id: Optional[UUID] = None
    academic_year: Optional[str] = None
    pledge_amount: Optional[Decimal] = Field(None, ge=0)
    approved_amount: Optional[Decimal] = Field(None, ge=0)
    funded_amount: Optional[Decimal] = Field(None, ge=0)
    status: Optional[GassoStatus] = None
    soft_credit_applied: Optional[bool] = None
    stage_history: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class GassoRecordResponse(GassoRecordBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
