from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey, JSON, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..database import Base, UUID, is_sqlite

# INET type for SQLite compatibility
if is_sqlite:
    INET = String(45)  # IPv6 max length
else:
    from sqlalchemy.dialects.postgresql import INET


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    DEVELOPMENT = "development"
    EVENTS = "events"
    READ_ONLY = "read_only"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.READ_ONLY)
    
    # Flexible permissions JSON
    permissions = Column(JSON, default=dict)
    
    is_active = Column(Boolean, default=True)
    
    # MFA
    mfa_secret = Column(String(255), nullable=True)
    
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(UUID, nullable=True)
    
    # JSON of changes (before/after)
    changes = Column(JSON, default=dict)
    
    # IP address for security
    ip_address = Column(INET, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
