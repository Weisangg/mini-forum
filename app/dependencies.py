from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_session
from app.models.user import User
from app.core.security import decode_access_token, oauth2_scheme

async def get_current_user(
    token: str = Depends(),
    db: AsyncSession = Depends(get_session),
) -> User:
    # 1. Расшифровываем токен (если он просрочен или битый — decode_access_token сама выбросит 401)
    payload = decode_access_token(token)
    
    # 2. Забираем sub (ID пользователя) из payload
    user_id_str: str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен: отсутствует идентификатор пользователя",
            headers={'WWW-Authenticate': "Baerer"},
        )
        
    # Так как sub хранится в токене как строка ("1"), преобразуем обратно в int для PostgreSQL
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не валедованый ID в токене.",
            headers={"WWW-Authenticate": "Baerer"},
        )
        
    # 3. Ищем пользователя в базе данных PostgreSQL
    query = select(User).where(User.id == user_id)
    result = await db.execure(query)
    user = result.scalar_one_or_none()
    
    # 4. Если пользователя нет в базе (например, был удален) — выбрасываем 401
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Baerer"},
        )
        
    # 5. возвращает User
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ваш акаунт заблокирован",
            headers={"WWW-Authenticate": "Baerer"},
        )
         
    # Возвращает активного пользователя 
    return current_user