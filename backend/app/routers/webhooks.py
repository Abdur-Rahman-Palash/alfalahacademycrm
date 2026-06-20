from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(request: Request):
    # TODO: Implement Stripe webhook signature verification
    payload = await request.body()
    return {"message": "Stripe webhook received - Phase 2"}
