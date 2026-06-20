from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
import uuid
import enum

from ..database import Base, UUID, ARRAY


class ConstituentType(str, enum.Enum):
    INDIVIDUAL = "individual"
    FAMILY = "family"
    CORPORATE = "corporate"
    FOUNDATION = "foundation"


class Constituent(Base):
    __tablename__ = "constituents"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(SQLEnum(ConstituentType), nullable=False, default=ConstituentType.INDIVIDUAL)
    
    # Name fields
    first_name = Column(String(100))
    last_name = Column(String(100))
    org_name = Column(String(200))
    
    # Contact info
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    address = Column(JSON)  # {street, city, state, zip, country}
    
    # Stripe integration
    stripe_customer_id = Column(String(255))
    
    # Flexible attributes
    constituent_codes = Column(JSON, default=list)  # Up to 25 attributes
    communication_prefs = Column(JSON, default=dict)  # {email: bool, sms: bool, mail: bool}
    
    # Flags
    is_donor = Column(Boolean, default=False)
    is_parent = Column(Boolean, default=False)
    is_alumni = Column(Boolean, default=False)
    is_volunteer = Column(Boolean, default=False)
    
    # Status
    status = Column(String(50), default="active")
    
    # Soft delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
