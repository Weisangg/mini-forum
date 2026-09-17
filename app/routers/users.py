from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.db.database import get_session
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/",response_model=list[UserResponse])
async def register_categories(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    existing_user = await db.execute(
        select(User).where((User.email == user_in.email) | (User.userm)) 
    )

@router.get("/{category_id}", response_model=UserResponse)
async def register_categories_id(category_in: UserCreate, db: AsyncSession = Depends(get_session)):
    category = await db.execute(User, category_in)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.get("/me", response_model=UserResponse)
async def get_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_session),
    currend_user: User = Depends(get_current_user)
):
    """Частичное обновление профиля текущего пользователя"""
    
    # 1. Проверяем уникальность username, если его хотят изменить
    if user_in.username is not None and user_in.username != currend_user.username:
        result = await db.execute(
            select(User).where(User.username == user_in.username)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This email is already registered.',
            )
            
    # 3. Извлекаем только те поля, которые клиент передал в запросе
    update_data = user_in.model_dump(exclude_unset=True)
    
    # 4. Обновляем поля у текущего пользователя
    for field, value in update_data.items():
        setattr(currend_user, field, value)
        
    # 5. Сохраняем в БД
    db.add(currend_user)
    await db.commit()
    await db.refresh(currend_user)

    return currend_user