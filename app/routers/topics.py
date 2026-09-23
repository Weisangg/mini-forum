from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic
from app.models.user import User
from app.models.category import Category
from app.schemas.topic import TopicCreate, TopicResponse, TopicUpdate, TopicDetailResponse
from app.db.database import get_session

from app.dependencies import get_current_user

router = APIRouter(prefix='/topics',tags=['Topics'])

@router.get('/', response_model=list[TopicResponse])
async def register_topics(
    search: str | None = Query(None, description="Поиск по названию темы"),
    category_id: int = Query(None, description="Фильтр по категории"),
    author_id: int | None = Query(None, description="Фильтр по автору"),
    limit: int = Query(10, ge=1, le=100, description="Колисество тем"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_session)
):
    stmt = select(Topic)
    
    # 1. Фильтрация
    if search:
        stmt = stmt.where(Topic.title.ilike(f"%{search}%"))
    if category_id is not None:
        stmt = stmt.where(Topic.category_id == category_id)
    if author_id is not None:
        stmt = stmt.where(Topic.author_id == author_id)
        
    # 2. Пагинация
    stmt = stmt.offset(offset).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()

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

# 1. PATCH /topics/{topic_id} — Редактирование
@router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    
    topic_id: int,
    topic_data: TopicUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    
    # Поиск темы в БД
    topic = await db.get(Topic, topic_id)
    
    # 1. Проверка на существование (404 Not Found)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )
        
    # 2. Проверка автора
    if topic.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own topics"
        )
        
    # Обновление только переданных полей (exclude_unset=True)
    update_dict = topic_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(topic, key, value)
        
    await db.commit()
    await db.refresh(topic)
    
    return topic

# 2. DELETE /topics/{topic_id} — Удаление
@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: int,
    db: AsyncSession = Depends(get_session),
    curren_user: User = Depends(get_current_user)
):
    topic = await db.get(Topic, topic_id)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="topic not fount",
        )
        
    # Проверка автора
    if topic.author_id != curren_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own topics",
        )
    
    await db.delete(topic)
    await db.commit()
    
    return None

@router.get("/{topic_id}", response_model=TopicDetailResponse)
async def get_topic_detail(
    topic_id: int,
    db: AsyncSession = Depends(get_session)
):
    stmt = select(Topic).options(selectinload(Topic.posts)).where(Topic.id == topic_id)
    result = await db.execute(stmt)
    topic = result.scalar_one_or_none()
    
    if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="topic not fount",
            )
    
    return topic
    