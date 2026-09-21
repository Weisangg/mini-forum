from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserResponse

class PostBase(BaseModel):
    content: str = Field(min_length=1, max_length=5000, description="Текст сообщение")
    
class PostCreate(PostBase):
    topic_id: int
    
class PostResponse(PostBase):
    id: int
    author_id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    
class PostDetailResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    
    author: UserResponse
    
    likes_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)