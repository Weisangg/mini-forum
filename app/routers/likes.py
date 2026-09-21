from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic
from app.models.user import User
from app.models.post import Post
from app.models.like import Like
from app.models.category import Category
from app.schemas.like import LikeResponse, LikeCreate
from app.db.database import get_session

from app.dependencies import get_current_user

router = APIRouter(tags=["Like"])

@router.post("/posts/{post_id}/likes", status_code=status.HTTP_201_CREATED)
async def add_like(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    stmt = select(Like).where(Like.user_id == current_user.id, Like.post_id == post_id)
    reselt = await db.execute(stmt)
    existing_like = reselt.scalar_one_or_none()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Лайк уже стоит"
        )
        
    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )
    
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like) # чтобы получить сгенерированный id

    return new_like

@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    stmt = select(Like).where(Like.user_id == current_user.id, Like.post_id == post_id)
    result = await db.execute(stmt)
    existing_like = result.scalar_one_or_none()
    
    if not existing_like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Удалять нечего"
        )
    
    await db.delete(existing_like)
    await db.commit()
    
    return None