from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic
from app.models.user import User
from app.models.post import Post
from app.models.category import Category
from app.schemas.post import PostCreate,PostUpdate ,PostResponse
from app.db.database import get_session

from app.dependencies import get_current_user

router = APIRouter(tags=["Posts"])

# 1. Читать могут все: НЕТ зависимости get_current_user
@router.get("/topics/{topic_id}/posts", response_model=list[PostResponse])
async def get_posts_for_topic(
    topic_id: int, 
    db: AsyncSession = Depends(get_session)
):
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У вас нет темы",
        )
        
    stmt = select(Post).where(Post.topic_id == topic_id)
    result = await db.execute(stmt)
    
    return result.scalars().all

# 2. POST /topics/{topic_id}/posts — Создание сообщения (Только авторизованные)
@router.post("/topics/{topic_id}/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    topic_id: int,
    post_in: PostCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    #1. Проверить существование темы (404 если тема не найдена)
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У вас нет темы",
        )
    
    # 2. Создать объект модели Post
    # Обрати внимание: content берем из post_in, topic_id из URL, а author_id СТРОГО из current_user.id        
    new_post = Post(
        content=post_in.content,
        topic_id=topic_id.topic_id,
        author_id=current_user.id
    )
    
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    return new_post

@router.patch("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    post = await db.get(Post, post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение нет"
        )
    
    # Если это чужое сообщение — выбросить HTTPException 403 Forbidden    
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы модете редактировать только свои сообщения"
        )
    
    post.content = post.content = post_in.content
    
    await db.commit()
    await db.refresh(post)
    
    return post

# 4. DELETE /posts/{post_id} — Удаление сообщения
@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    post = await db.get(Post, post_id)
    # Проверка существует ли post
    if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сообщение нет"
            )
    
    if post.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы модете редактировать только свои сообщения"
            )
            
    await db.delete(post)
    await db.commit()
    
    return None