from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.topic import Topic
    from app.models.like import Like

class User(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    topics: Mapped[list['Topic']] = relationship(back_populates="author", cascade="all, delete-orphan")
    posts: Mapped[list['Post']] = relationship(back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[list['Like']] = relationship(back_populates="author", cascade="all, delete-orphan")