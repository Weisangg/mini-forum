from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from datetime import datetime, timezone

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.topic import Topic

class Category(Base):
    __tablename__="categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    topics: Mapped[list["Topic"]] = relationship(back_populates="author", cascade="all, delete-orphan")