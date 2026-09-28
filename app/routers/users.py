from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.db.database import get_session
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    """Отримання списку всіх користувачів"""
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Отримання інформації про поточного авторизованого користувача"""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_user_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Часткове оновлення профілю поточного користувача"""
    
    # 1. Перевіряємо унікальність username, якщо користувач його змінює
    if user_in.username is not None and user_in.username != current_user.username:
        result = await db.execute(
            select(User).where(User.username == user_in.username)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is already taken.",
            )
            
    # 2. Отримуємо тільки передані поля
    update_data = user_in.model_dump(exclude_unset=True)
    
    # 3. Оновлюємо атрибути об'єкта
    for field, value in update_data.items():
        setattr(current_user, field, value)
        
    # 4. Зберігаємо зміни в БД
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int, 
    db: AsyncSession = Depends(get_session)
):
    """Отримання користувача за ID"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user