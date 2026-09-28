from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.user import User
from app.core.security import decode_access_token, oauth2_scheme

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session),
) -> User:
    # 1. Розшифровуємо токен (якщо прострочений/невалідний — decode_access_token викидає 401)
    payload = decode_access_token(token)
    
    # 2. Отримуємо sub (ID користувача) з payload
    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалідний токен: відсутній ідентифікатор користувача",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалідний ID у токені",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Шукаємо користувача в БД
    user = await db.get(User, user_id)
    
    # 4. Якщо користувача немає в БД
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Обліковий запис заблоковано",
            headers={"WWW-Authenticate": "Bearer"},
        )
         
    return current_user