from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime, timezone

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.topic import Topic

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True, default=None)  # <- nullable=True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    topics: Mapped[list["Topic"]] = relationship(back_populates="category", cascade="all, delete-orphan")