from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..models.scholarship import GassoRecord
from ..models.user import User
from ..schemas.scholarship import GassoRecordCreate, GassoRecordUpdate, GassoRecordResponse
from ..auth import get_current_user, require_role, UserRole

router = APIRouter()


@router.post("/", response_model=GassoRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_gasso_record(
    record: GassoRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    db_record = GassoRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record


@router.get("/", response_model=List[GassoRecordResponse])
async def list_gasso_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    academic_year: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(GassoRecord)
    
    if academic_year:
        query = query.filter(GassoRecord.academic_year == academic_year)
    
    if status:
        query = query.filter(GassoRecord.status == status)
    
    records = query.order_by(GassoRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records


@router.get("/{record_id}", response_model=GassoRecordResponse)
async def get_gasso_record(
    record_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(GassoRecord).filter(GassoRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GaSSO record not found",
        )
    
    return record


@router.put("/{record_id}", response_model=GassoRecordResponse)
async def update_gasso_record(
    record_id: UUID,
    record_update: GassoRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    record = db.query(GassoRecord).filter(GassoRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GaSSO record not found",
        )
    
    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record
