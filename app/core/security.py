import jwt 
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jwt.exceptions import ExpiredSignatureError, PyJWKError
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session

SEKRET_KEY = "gggself"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # schemes превращает пароль в хэшированый и auto то что при обнавлении старые даные перепишуться под новые

def password_hash(password):
    return pwd_context.hash(password)

def password_verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    playoad = {
        'sub': str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    
    # генерируюет токен и подписываем playoad
    token = jwt.encode(playoad, SEKRET_KEY, algorithm=ALGORITHM)
    
    # возвращает токен
    return token

def decode_access_token(token: str) -> dict:
    try:
        # 1. Проверяем подпись и расшифровываем payload
        payload = jwt.encode(token, SEKRET_KEY, algorithm=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # 2. Срок действия токена истек (прошло больше 60 минут)
        raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Срок действия токена истек. Войдите заново в систему.",
              headeres={'WWW-Authententicate': "Bearer"},
          )
        
    except PyJWKError:
        # 3. Токен подделан, поврежден или недействителен
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен авторизации.",
            headeres={'WWW-Authententicate': 'Bearer'},
        )
        
