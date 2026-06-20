from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..models.event import Event, Ticket
from ..models.user import User
from ..schemas.event import EventCreate, EventUpdate, EventResponse, TicketCreate, TicketResponse
from ..auth import get_current_user, require_role, UserRole

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EVENTS]))
):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event


@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status)
    
    events = query.order_by(Event.date.desc()).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EVENTS]))
):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    
    return event


# Tickets
@router.post("/{event_id}/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    event_id: UUID,
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EVENTS]))
):
    import uuid
    import secrets
    
    # Generate unique QR code
    qr_code = secrets.token_urlsafe(16)
    
    db_ticket = Ticket(
        event_id=event_id,
        constituent_id=ticket.constituent_id,
        ticket_type=ticket.ticket_type,
        qr_code=qr_code,
        amount_paid=ticket.amount_paid,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket


@router.get("/{event_id}/tickets", response_model=List[TicketResponse])
async def list_event_tickets(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tickets = db.query(Ticket).filter(Ticket.event_id == event_id).all()
    return tickets


@router.post("/{event_id}/tickets/{ticket_id}/checkin")
async def check_in_ticket(
    event_id: UUID,
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EVENTS]))
):
    from datetime import datetime
    
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.event_id == event_id
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    if ticket.checked_in_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket already checked in",
        )
    
    ticket.checked_in_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Check-in successful"}
