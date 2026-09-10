from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import password_hash
from app.db.database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

# Прежде чем запустить регистрацию пользователя, выполни функцию get_session(Depends)
@router.post("/register", response_model="UserResponse", status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    
    # 1. Проверяем, свободен ли email и username
    query = select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        if existing_user.email == user_in.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Имя пользователя уже занято"
        )
        
    # 2. Хешируем пароль
    hashed_pwd = password_hash(user_in.password)
        
    new_user = User(
        username = user_in.username,
        email=user_in.email,
        hashed_password=hashed_pwd
    )
        
    # 4. Сохраняем в PostgreSQL
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
        
    # 5. Возвращаем объект (FastAPI отфильтрует его через UserResponse)
    return new_user