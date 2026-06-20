from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Numeric, ForeignKey, Text, JSON, Boolean
from sqlalchemy.sql import func
import uuid
import enum

from ..database import Base, UUID, ARRAY


class GassoStatus(str, enum.Enum):
    PLEDGED = "pledged"
    APPROVED = "approved"
    PARTIALLY_FUNDED = "partially_funded"
    FULLY_FUNDED = "fully_funded"
    DENIED = "denied"


class GassoRecord(Base):
    __tablename__ = "gasso_records"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(UUID, nullable=False)  # References JupiterEd student
    constituent_id = Column(UUID, ForeignKey("constituents.id"), nullable=False)
    
    academic_year = Column(String(20), nullable=False)  # e.g., "2024-2025"
    
    # Monetary values
    pledge_amount = Column(Numeric(precision=10, scale=2), nullable=False)
    approved_amount = Column(Numeric(precision=10, scale=2), nullable=True)
    funded_amount = Column(Numeric(precision=10, scale=2), default=0)
    
    status = Column(SQLEnum(GassoStatus), nullable=False, default=GassoStatus.PLEDGED)
    
    soft_credit_applied = Column(Boolean, default=False)
    
    # Full audit trail of stage changes
    stage_history = Column(ARRAY(JSON), default=list)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
