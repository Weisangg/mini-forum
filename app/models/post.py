from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.like import Like
    from app.models.user import User
    from app.models.topic import Topic
    
    
class Post(Base):
    __tablename__="Post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", "CASCADE"),
        nullable=False
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", "CASCADE"),
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
    user: Mapped[list["User"]] = relationship(back_populates='posts')
    topic: Mapped[list["Topic"]] = relationship(back_populates='posts')
    
    # Связь: тема -> сообщения (1 ко многим)
    likes: Mapped[list["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")