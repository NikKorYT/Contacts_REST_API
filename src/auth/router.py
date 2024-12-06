from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from config.db import get_db
from src.auth.pass_utils import verify_password
from src.auth.repo import UserRepository
from src.auth.schemas import UserCreate, Token
from src.auth.utils import create_access_token, create_refresh_token, decode_access_token


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

@router.post("/token", response_model=Token)
async def login_for_access_token(
    from_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):   
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(from_data.username)
    if not user or not verify_password(from_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)  

@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_token: str, db: AsyncSession = Depends(get_db)
):
    token_data = decode_access_token(refresh_token)
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
