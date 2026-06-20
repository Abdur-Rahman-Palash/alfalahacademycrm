from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import stripe
from datetime import datetime
import json

from ..database import get_db
from ..models.donor import Constituent
from ..models.donation import Donation, RecurringSchedule
from ..models.campaign import Campaign
from ..config import settings
from ..schemas.payment import (
    PaymentIntentRequest,
    PaymentIntentResponse,
    SubscriptionRequest,
    SubscriptionResponse
)

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    request: PaymentIntentRequest,
    db: Session = Depends(get_db)
):
    """
    Create a Stripe payment intent for one-time or recurring donations
    """
    try:
        # Find or create donor
        donor = db.query(Constituent).filter(
            Constituent.email == request.donor.email
        ).first()
        
        if not donor:
            donor = Constituent(
                first_name=request.donor.firstName,
                last_name=request.donor.lastName,
                email=request.donor.email,
                phone=request.donor.phone,
                address={"street": request.donor.address, "city": request.donor.city, "state": request.donor.state, "zip": request.donor.zip} if request.donor.address else None,
                is_donor=True,
                status="active"
            )
            db.add(donor)
            db.commit()
            db.refresh(donor)
        else:
            # Update existing constituent info
            donor.first_name = request.donor.firstName
            donor.last_name = request.donor.lastName
            donor.phone = request.donor.phone
            if request.donor.address:
                donor.address = {"street": request.donor.address, "city": request.donor.city, "state": request.donor.state, "zip": request.donor.zip}
            db.commit()
        
        # Create payment intent
        payment_intent_data = {
            "amount": request.amount,
            "currency": request.currency,
            "metadata": {
                "donor_id": str(donor.id),
                "frequency": request.frequency,
                "campaign_id": request.campaignId or "",
                "is_anonymous": str(request.isAnonymous),
                "dedication": json.dumps(request.dedication.dict()) if request.dedication else ""
            },
            "description": f"Donation from {donor.first_name} {donor.last_name}"
        }
        
        # Add customer information
        if donor.stripe_customer_id:
            payment_intent_data["customer"] = donor.stripe_customer_id
        else:
            # Create Stripe customer
            address_data = None
            if donor.address and isinstance(donor.address, dict):
                address_data = {
                    "line1": donor.address.get("street"),
                    "city": donor.address.get("city"),
                    "state": donor.address.get("state"),
                    "postal_code": donor.address.get("zip")
                }
            
            customer = stripe.Customer.create(
                email=donor.email,
                name=f"{donor.first_name} {donor.last_name}",
                phone=donor.phone,
                address=address_data
            )
            donor.stripe_customer_id = customer.id
            db.commit()
            payment_intent_data["customer"] = customer.id
        
        payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
        
        return PaymentIntentResponse(
            clientSecret=payment_intent.client_secret,
            paymentIntentId=payment_intent.id,
            amount=request.amount / 100  # Convert back to dollars
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating payment intent: {str(e)}"
        )


@router.post("/create-subscription", response_model=SubscriptionResponse)
async def create_subscription(
    request: SubscriptionRequest,
    db: Session = Depends(get_db)
):
    """
    Create a Stripe subscription for recurring donations
    """
    try:
        # Find or create donor
        donor = db.query(Constituent).filter(
            Constituent.email == request.donor.email
        ).first()
        
        if not donor:
            donor = Constituent(
                first_name=request.donor.firstName,
                last_name=request.donor.lastName,
                email=request.donor.email,
                phone=request.donor.phone,
                address={"street": request.donor.address, "city": request.donor.city, "state": request.donor.state, "zip": request.donor.zip} if request.donor.address else None,
                is_donor=True,
                status="active"
            )
            db.add(donor)
            db.commit()
            db.refresh(donor)
        
        # Create or get Stripe customer
        if not donor.stripe_customer_id:
            address_data = None
            if donor.address and isinstance(donor.address, dict):
                address_data = {
                    "line1": donor.address.get("street"),
                    "city": donor.address.get("city"),
                    "state": donor.address.get("state"),
                    "postal_code": donor.address.get("zip")
                }
            
            customer = stripe.Customer.create(
                email=donor.email,
                name=f"{donor.first_name} {donor.last_name}",
                phone=donor.phone,
                address=address_data
            )
            donor.stripe_customer_id = customer.id
            db.commit()
        
        # Create price for the subscription amount
        price = stripe.Price.create(
            unit_amount=request.amount,
            currency=request.currency,
            recurring={
                "interval": request.frequency,  # month or year
                "interval_count": 1
            },
            product_data={
                "name": f"Recurring Donation - {request.frequency}ly"
            }
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=donor.stripe_customer_id,
            items=[{"price": price.id}],
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=["latest_invoice.payment_intent"],
            metadata={
                "donor_id": str(donor.id),
                "campaign_id": request.campaignId or "",
                "is_anonymous": str(request.isAnonymous)
            }
        )
        
        # Create recurring schedule record
        recurring_schedule = RecurringSchedule(
            donor_id=donor.id,
            amount=request.amount / 100,
            frequency=request.frequency,
            start_date=datetime.now().date(),
            stripe_subscription_id=subscription.id,
            status="active",
            campaign_id=request.campaignId
        )
        db.add(recurring_schedule)
        db.commit()
        
        return SubscriptionResponse(
            subscriptionId=subscription.id,
            clientSecret=subscription.latest_invoice.payment_intent.client_secret,
            amount=request.amount / 100,
            frequency=request.frequency
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating subscription: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        await handle_payment_success(payment_intent, db)
    elif event.type == "payment_intent.payment_failed":
        payment_intent = event.data.object
        await handle_payment_failure(payment_intent, db)
    elif event.type == "invoice.payment_succeeded":
        invoice = event.data.object
        await handle_recurring_payment_success(invoice, db)
    elif event.type == "invoice.payment_failed":
        invoice = event.data.object
        await handle_recurring_payment_failure(invoice, db)
    elif event.type == "customer.subscription.deleted":
        subscription = event.data.object
        await handle_subscription_cancellation(subscription, db)
    
    return JSONResponse(status_code=200, content={"status": "success"})


async def handle_payment_success(payment_intent: stripe.PaymentIntent, db: Session):
    """Handle successful payment intent"""
    donor_id = payment_intent.metadata.get("donor_id")
    frequency = payment_intent.metadata.get("frequency", "one_time")
    campaign_id = payment_intent.metadata.get("campaign_id")
    is_anonymous = payment_intent.metadata.get("is_anonymous", "false") == "true"
    
    # Create donation record
    donation = Donation(
        donor_id=donor_id,
        amount=payment_intent.amount / 100,
        currency=payment_intent.currency,
        payment_method="stripe",
        payment_status="completed",
        donation_type="recurring" if frequency != "one_time" else "one_time",
        frequency=frequency if frequency != "one_time" else None,
        campaign_id=campaign_id if campaign_id else None,
        is_anonymous=is_anonymous,
        stripe_payment_intent_id=payment_intent.id,
        payment_date=datetime.now()
    )
    
    # Add dedication if present
    if payment_intent.metadata.get("dedication"):
        dedication_data = json.loads(payment_intent.metadata["dedication"])
        donation.dedication_type = dedication_data.get("type")
        donation.dedication_name = dedication_data.get("name")
        donation.dedication_email = dedication_data.get("email")
    
    db.add(donation)
    
    # Update campaign total if applicable
    if campaign_id:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.raised_amount += payment_intent.amount / 100
    
    db.commit()


async def handle_payment_failure(payment_intent: stripe.PaymentIntent, db: Session):
    """Handle failed payment intent"""
    donor_id = payment_intent.metadata.get("donor_id")
    
    donation = Donation(
        donor_id=donor_id,
        amount=payment_intent.amount / 100,
        currency=payment_intent.currency,
        payment_method="stripe",
        payment_status="failed",
        donation_type="one_time",
        stripe_payment_intent_id=payment_intent.id,
        payment_date=datetime.now()
    )
    
    db.add(donation)
    db.commit()


async def handle_recurring_payment_success(invoice: stripe.Invoice, db: Session):
    """Handle successful recurring payment"""
    subscription_id = invoice.subscription
    recurring_schedule = db.query(RecurringSchedule).filter(
        RecurringSchedule.stripe_subscription_id == subscription_id
    ).first()
    
    if recurring_schedule:
        donation = Donation(
            donor_id=recurring_schedule.donor_id,
            amount=invoice.amount_paid / 100,
            currency=invoice.currency,
            payment_method="stripe",
            payment_status="completed",
            donation_type="recurring",
            frequency=recurring_schedule.frequency,
            recurring_schedule_id=recurring_schedule.id,
            campaign_id=recurring_schedule.campaign_id,
            stripe_payment_intent_id=invoice.payment_intent,
            payment_date=datetime.now()
        )
        
        db.add(donation)
        
        # Update campaign total if applicable
        if recurring_schedule.campaign_id:
            campaign = db.query(Campaign).filter(
                Campaign.id == recurring_schedule.campaign_id
            ).first()
            if campaign:
                campaign.raised_amount += invoice.amount_paid / 100
        
        # Update recurring schedule
        recurring_schedule.last_payment_date = datetime.now().date()
        recurring_schedule.next_payment_date = datetime.now().date()
        
        db.commit()


async def handle_recurring_payment_failure(invoice: stripe.Invoice, db: Session):
    """Handle failed recurring payment"""
    subscription_id = invoice.subscription
    recurring_schedule = db.query(RecurringSchedule).filter(
        RecurringSchedule.stripe_subscription_id == subscription_id
    ).first()
    
    if recurring_schedule:
        recurring_schedule.failed_attempts += 1
        
        if recurring_schedule.failed_attempts >= 3:
            recurring_schedule.status = "cancelled"
        
        db.commit()


async def handle_subscription_cancellation(subscription: stripe.Subscription, db: Session):
    """Handle subscription cancellation"""
    recurring_schedule = db.query(RecurringSchedule).filter(
        RecurringSchedule.stripe_subscription_id == subscription.id
    ).first()
    
    if recurring_schedule:
        recurring_schedule.status = "cancelled"
        recurring_schedule.end_date = datetime.now().date()
        db.commit()


@router.get("/donor/{donor_id}/donations")
async def get_donor_donations(
    donor_id: str,
    db: Session = Depends(get_db)
):
    """Get donation history for a specific donor"""
    donations = db.query(Donation).filter(
        Donation.donor_id == donor_id
    ).order_by(Donation.payment_date.desc()).all()
    
    return {
        "donations": donations,
        "total": sum(d.amount for d in donations),
        "count": len(donations)
    }


@router.get("/donor/{donor_id}/recurring")
async def get_donor_recurring(
    donor_id: str,
    db: Session = Depends(get_db)
):
    """Get recurring donation schedules for a specific donor"""
    schedules = db.query(RecurringSchedule).filter(
        RecurringSchedule.donor_id == donor_id,
        RecurringSchedule.status == "active"
    ).all()
    
    return {"schedules": schedules}
