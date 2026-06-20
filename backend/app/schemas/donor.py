from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from ..models.donor import ConstituentType


class ConstituentBase(BaseModel):
    type: ConstituentType = ConstituentType.INDIVIDUAL
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    org_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    constituent_codes: Optional[List[str]] = None
    communication_prefs: Optional[Dict[str, bool]] = None
    is_donor: bool = False
    is_parent: bool = False
    is_alumni: bool = False
    is_volunteer: bool = False


class ConstituentCreate(ConstituentBase):
    pass


class ConstituentUpdate(BaseModel):
    type: Optional[ConstituentType] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    org_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    constituent_codes: Optional[List[str]] = None
    communication_prefs: Optional[Dict[str, bool]] = None
    is_donor: Optional[bool] = None
    is_parent: Optional[bool] = None
    is_alumni: Optional[bool] = None
    is_volunteer: Optional[bool] = None


class ConstituentResponse(ConstituentBase):
    id: UUID
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
