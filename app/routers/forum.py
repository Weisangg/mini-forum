from fastapi import APIRouter

router = APIRouter(prefix="/forum", tags=["Forum"])

@router.get("/topics")
async def get_topics():
    return {"message": "Здесь будет список тем"}