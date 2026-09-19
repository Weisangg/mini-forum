from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.topic import TopicResponse

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    bio: str | None = Field(default=None, max_length=500)

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    bio: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default=None)
    bio: str | None = Field(default=None, max_length=500)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
UserResponse.model_rebuild()