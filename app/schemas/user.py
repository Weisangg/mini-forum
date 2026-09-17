from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.topic import TopicResponse

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    bio: str | None = Field(default=None, max_length=500)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    topics: list[TopicResponse] = []

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default=None)
    bio: str | None = Field(default=None, max_length=500)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
UserResponse.model_rebuild()