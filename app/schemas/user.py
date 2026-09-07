from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr

class UserCreat(UserBase):
    password: str = Field(min_length=8, max_length=20)

# 4. Исходящий ответ API
class UserResponse(UserBase):
    id: int 
    created_at: datetime
    is_active: bool
    
    # для чтения объектов из SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
    
class UserUpdata(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None # означает что поле по умолчанию пустое 
    password: Optional[str] = Field(None, min_length=8, max_length=20)
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"