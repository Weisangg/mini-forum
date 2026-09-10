# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from app.models.user import User
# from app.schemas.user import UserCreate, UserResponse
# from app.core.security import password_hash 
# from app.db.database import get_session

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/",response_model=list[UserResponse])
# async def register_categories(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
#     existing_user = await db.execute(
#         select(User).where((User.email == user_in.email) | (User.userm)) 
#     )

# @router.get("/{category_id}", response_model=UserResponse)
# async def register_categories_id(category_in: UserCreate, db: AsyncSession = Depends(get_session)):
#     category = await db.execute(User, category_in)
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
#     return category