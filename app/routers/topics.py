from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic
from app.models.user import User
from app.models.category import Category
from app.schemas.topic import TopicCreate, TopicResponse
from app.db.database import get_session

from app.dependencies import get_current_user

router = APIRouter(prefix='/topics',tags=['Topics'])

@router.get('/', response_model=list[TopicResponse])
async def register_topics(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Topic))
    return result.scalars().all

@router.get("/{topic_id}", response_model=TopicResponse)
async def register_topics_id(topic_id: int, db: AsyncSession = Depends(get_session)):
    """Получить конкретную категорию по ID"""
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )
    return topic

# 3. POST /topics — Создать новую тему
@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_in: TopicCreate, 
    db: AsyncSession = Depends(get_session),
    # Правило 2: Защита эндпоинта — сюда попадает только авторизованный юзер
    current_user: User = Depends(get_current_user)
    ):
    
    # Правило 3: Проверяем, существует ли указанная категория
    category = await db.get(Category, topic_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with is {topic_in.category_id} does not exist",
        )
        
    # Правило 4: ID автора берём из JWT (из объекта current_user)
    new_topic = Topic(
        **topic_in.model_dump(),
        author_id=current_user.id # Подставляем ID текущего юзера
    )
    
    
    # 4. Сохраняем в PostgreSQL
    db.add(new_topic)
    await db.commit()
    await db.refresh(new_topic)
    
    # 5. Возврощает новою тему
    return new_topic