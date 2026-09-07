from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    content: str = Field(None, min_length=1)
    
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