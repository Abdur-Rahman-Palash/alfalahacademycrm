from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_reports():
    return {"message": "Reports module - Phase 2"}
