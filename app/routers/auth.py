from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import password_hash, password_verify, create_access_token
from app.db.database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

async def authenticate_user(db: AsyncSession, username_or_email: str, password: str):
    stmt = select(User).where((User.email == username_or_email) | (User.username == username_or_email))
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user or not password_verify(password, user.hashed_password):
        return None
    return user

# Прежде чем запустить регистрацию пользователя, выполни функцию get_session(Depends)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
    username=user_in.username,
    email=user_in.email,
    hashed_password=hashed_pwd,
    bio=user_in.bio,  
)
        
    # 4. Сохраняем в PostgreSQL
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
        
    # 5. Возвращаем объект (FastAPI отфильтрует его через UserResponse)
    return new_user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    
    # 2. Проверяем существование и пароль
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Создаем токен
    token = create_access_token(user_id=user.id)
    
    # 4. Возвращает результат 
    return {
        "access_token": token,
        "token_type": "bearer"
    }