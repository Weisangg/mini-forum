from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TopicBase(BaseModel):
    title: str = Field(None, min_length=5, max_length=255)
    
class TopicCreate(TopicBase):
    category_id: int

class TopicResponse(TopicBase):
    id: int
    category_id: int
    author_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class TopicUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=255) 
    

