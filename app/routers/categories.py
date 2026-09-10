from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.security import password_hash 
from app.db.database import get_session

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/",response_model=list[CategoryResponse])
async def register_categories(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Category))
    return result.scalars().all

@router.get("/{category_id}", response_model=CategoryResponse)
async def register_categories_id(category_in: CategoryCreate, db: AsyncSession = Depends(get_session)):
    """Получить конкретную категорию по ID"""
    category = await db.execute(Category, category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category