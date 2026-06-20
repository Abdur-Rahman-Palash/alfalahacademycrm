from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_communications():
    return {"message": "Communications module - Phase 2"}
