import stripe
from typing import Dict, Optional, List
from decimal import Decimal
from datetime import datetime
from ..config import settings

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for Stripe payment processing."""
    
    @staticmethod
    async def create_payment_intent(
        amount: Decimal,
        currency: str = "usd",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Stripe PaymentIntent for one-time payments.
        
        Args:
            amount: Payment amount in cents (multiply dollars by 100)
            currency: Currency code (default: usd)
            metadata: Additional metadata to attach to the payment
        
        Returns:
            PaymentIntent object
        """
        try:
            amount_cents = int(amount * 100)
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            
            return {
                "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id,
                "amount": amount,
                "currency": currency
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def create_customer(
        email: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Create a Stripe customer.
        
        Returns:
            Customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                phone=phone,
                metadata=metadata or {}
            )
            return customer.id
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def create_subscription(
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Stripe subscription for recurring donations.
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID for the subscription
            metadata: Additional metadata
        
        Returns:
            Subscription object
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                metadata=metadata or {},
                payment_behavior="default_incomplete",
                payment_settings={
                    "payment_method_types": ["card"],
                    "save_default_payment_method": "on_subscription",
                },
                expand=["latest_invoice.payment_intent"],
            )
            
            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "status": subscription.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def pause_subscription(subscription_id: str) -> Dict:
        """
        Pause a Stripe subscription.
        """
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                pause_collection={"behavior": "keep_as_draft"}
            )
            return {"status": subscription.status}
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def cancel_subscription(subscription_id: str) -> Dict:
        """
        Cancel a Stripe subscription at the end of the current billing period.
        """
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return {"status": subscription.status}
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def create_recurring_price(
        amount: Decimal,
        currency: str = "usd",
        interval: str = "month"
    ) -> str:
        """
        Create a recurring price for subscriptions.
        
        Returns:
            Price ID
        """
        try:
            amount_cents = int(amount * 100)
            
            price = stripe.Price.create(
                unit_amount=amount_cents,
                currency=currency,
                recurring={"interval": interval},
                product_data={"name": f"Recurring Donation - ${amount}/{interval}"}
            )
            
            return price.id
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def retrieve_payment_intent(payment_intent_id: str) -> Dict:
        """
        Retrieve a PaymentIntent to check its status.
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "id": payment_intent.id,
                "status": payment_intent.status,
                "amount": payment_intent.amount / 100,
                "currency": payment_intent.currency,
                "metadata": payment_intent.metadata
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def handle_webhook(payload: bytes, sig_header: str) -> Dict:
        """
        Handle Stripe webhook events.
        
        Args:
            payload: Raw webhook payload
            sig_header: Stripe signature header
        
        Returns:
            Event data
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            
            # Handle specific events
            if event.type == "payment_intent.succeeded":
                payment_intent = event.data.object
                return {
                    "type": "payment_succeeded",
                    "payment_intent_id": payment_intent.id,
                    "amount": payment_intent.amount / 100,
                    "metadata": payment_intent.metadata
                }
            
            elif event.type == "payment_intent.payment_failed":
                payment_intent = event.data.object
                return {
                    "type": "payment_failed",
                    "payment_intent_id": payment_intent.id,
                    "error": payment_intent.last_payment_error
                }
            
            elif event.type == "customer.subscription.created":
                subscription = event.data.object
                return {
                    "type": "subscription_created",
                    "subscription_id": subscription.id,
                    "customer_id": subscription.customer
                }
            
            elif event.type == "customer.subscription.deleted":
                subscription = event.data.object
                return {
                    "type": "subscription_cancelled",
                    "subscription_id": subscription.id,
                    "customer_id": subscription.customer
                }
            
            elif event.type == "invoice.payment_succeeded":
                invoice = event.data.object
                return {
                    "type": "invoice_paid",
                    "invoice_id": invoice.id,
                    "subscription_id": invoice.subscription,
                    "amount": invoice.amount_paid / 100
                }
            
            else:
                return {"type": "unhandled", "event_type": event.type}
                
        except ValueError as e:
            raise Exception(f"Invalid payload: {str(e)}")
        except stripe.error.SignatureVerificationError as e:
            raise Exception(f"Invalid signature: {str(e)}")
    
    @staticmethod
    async def get_customer_payment_methods(customer_id: str) -> List[Dict]:
        """
        Get all payment methods for a customer.
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            
            return [
                {
                    "id": pm.id,
                    "brand": pm.card.brand,
                    "last4": pm.card.last4,
                    "exp_month": pm.card.exp_month,
                    "exp_year": pm.card.exp_year
                }
                for pm in payment_methods.data
            ]
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
    
    @staticmethod
    async def create_refund(
        payment_intent_id: str,
        amount: Optional[Decimal] = None
    ) -> Dict:
        """
        Create a refund for a payment.
        
        Args:
            payment_intent_id: ID of the PaymentIntent to refund
            amount: Amount to refund in cents (None for full refund)
        """
        try:
            refund_params = {"payment_intent": payment_intent_id}
            
            if amount:
                refund_params["amount"] = int(amount * 100)
            
            refund = stripe.Refund.create(**refund_params)
            
            return {
                "refund_id": refund.id,
                "amount": refund.amount / 100,
                "status": refund.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
