from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.category import Category
    from app.models.user import User
class Topic(Base):
    __tablename__='topic'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    # Связи (многие к 1)
    authot: Mapped[list["User"]] = relationship(back_populates="posts")
    topic: Mapped[list["Topic"]] = relationship(back_populates="posts")
            
    # Связь: тема -> сообщения (1 ко многим)
    posts: Mapped[list["Post"]] = relationship(back_populates="post", cascade="all, delete-orphan")