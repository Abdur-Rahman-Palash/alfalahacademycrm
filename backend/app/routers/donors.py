from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..models.donor import Constituent
from ..models.user import User
from ..schemas.donor import ConstituentCreate, ConstituentUpdate, ConstituentResponse
from ..auth import get_current_user, require_role, UserRole

router = APIRouter()


@router.post("/", response_model=ConstituentResponse, status_code=status.HTTP_201_CREATED)
async def create_constituent(
    constituent: ConstituentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    # Check if email already exists
    existing = db.query(Constituent).filter(Constituent.email == constituent.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    db_constituent = Constituent(**constituent.model_dump())
    db.add(db_constituent)
    db.commit()
    db.refresh(db_constituent)
    
    return db_constituent


@router.get("/", response_model=List[ConstituentResponse])
async def list_constituents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Constituent).filter(Constituent.deleted_at.is_(None))
    
    if search:
        query = query.filter(
            (Constituent.first_name.ilike(f"%{search}%")) |
            (Constituent.last_name.ilike(f"%{search}%")) |
            (Constituent.email.ilike(f"%{search}%")) |
            (Constituent.org_name.ilike(f"%{search}%"))
        )
    
    constituents = query.offset(skip).limit(limit).all()
    return constituents


@router.get("/{constituent_id}", response_model=ConstituentResponse)
async def get_constituent(
    constituent_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    constituent = db.query(Constituent).filter(
        Constituent.id == constituent_id,
        Constituent.deleted_at.is_(None)
    ).first()
    
    if not constituent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Constituent not found",
        )
    
    return constituent


@router.put("/{constituent_id}", response_model=ConstituentResponse)
async def update_constituent(
    constituent_id: UUID,
    constituent_update: ConstituentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    constituent = db.query(Constituent).filter(
        Constituent.id == constituent_id,
        Constituent.deleted_at.is_(None)
    ).first()
    
    if not constituent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Constituent not found",
        )
    
    update_data = constituent_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(constituent, field, value)
    
    db.commit()
    db.refresh(constituent)
    
    return constituent


@router.delete("/{constituent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_constituent(
    constituent_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN]))
):
    constituent = db.query(Constituent).filter(
        Constituent.id == constituent_id,
        Constituent.deleted_at.is_(None)
    ).first()
    
    if not constituent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Constituent not found",
        )
    
    # Soft delete
    from datetime import datetime
    constituent.deleted_at = datetime.utcnow()
    db.commit()
    
    return None
