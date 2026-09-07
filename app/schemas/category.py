from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    description: str = Field(None, min_length=10, max_length=2000)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(BaseModel):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class CategoryUpdata(CategoryBase):
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    