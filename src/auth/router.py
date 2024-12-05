from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from config.db import get_db
from src.auth.repo import UserRepository
from src.auth.schemas import UserCreate, UserResponse


router = APIRouter()

@router.post("/register")
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detai="Username already exists",
        )
    user = await user_repo.create_user(user_create)
    return user
    