from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common import UserShort

class TopicBase(BaseModel):
    title: str = Field(min_length=5, max_length=255)

class TopicCreate(TopicBase):
    category_id: int

class TopicResponse(TopicBase):
    id: int
    category_id: int
    author_id: int
    created_at: datetime
    author: UserShort | None = None 

    model_config = ConfigDict(from_attributes=True)

class TopicUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=255)