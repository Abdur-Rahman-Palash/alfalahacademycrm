from fastapi import APIRouter

router = APIRouter()


@router.get("/give")
async def donation_portal():
    return {"message": "Donation portal - Phase 2"}
