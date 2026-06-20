from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..models.donation import Donation, RecurringSchedule
from ..models.user import User
from ..schemas.donation import DonationCreate, DonationUpdate, DonationResponse, RecurringScheduleCreate, RecurringScheduleUpdate, RecurringScheduleResponse
from ..auth import get_current_user, require_role, UserRole

router = APIRouter()


@router.post("/", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    db_donation = Donation(**donation.model_dump())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    
    return db_donation


@router.get("/", response_model=List[DonationResponse])
async def list_donations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    constituent_id: Optional[UUID] = None,
    campaign_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Donation)
    
    if constituent_id:
        query = query.filter(Donation.constituent_id == constituent_id)
    
    if campaign_id:
        query = query.filter(Donation.campaign_id == campaign_id)
    
    donations = query.order_by(Donation.created_at.desc()).offset(skip).limit(limit).all()
    return donations


@router.get("/{donation_id}", response_model=DonationResponse)
async def get_donation(
    donation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )
    
    return donation


@router.put("/{donation_id}", response_model=DonationResponse)
async def update_donation(
    donation_id: UUID,
    donation_update: DonationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )
    
    update_data = donation_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(donation, field, value)
    
    db.commit()
    db.refresh(donation)
    
    return donation


# Recurring Schedules
@router.post("/recurring/", response_model=RecurringScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_recurring_schedule(
    schedule: RecurringScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    db_schedule = RecurringSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    
    return db_schedule


@router.get("/recurring/", response_model=List[RecurringScheduleResponse])
async def list_recurring_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    constituent_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(RecurringSchedule)
    
    if constituent_id:
        query = query.filter(RecurringSchedule.constituent_id == constituent_id)
    
    schedules = query.offset(skip).limit(limit).all()
    return schedules


@router.put("/recurring/{schedule_id}", response_model=RecurringScheduleResponse)
async def update_recurring_schedule(
    schedule_id: UUID,
    schedule_update: RecurringScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.DEVELOPMENT]))
):
    schedule = db.query(RecurringSchedule).filter(RecurringSchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring schedule not found",
        )
    
    update_data = schedule_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(schedule, field, value)
    
    db.commit()
    db.refresh(schedule)
    
    return schedule
