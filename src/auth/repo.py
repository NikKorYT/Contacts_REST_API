from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.pass_utils import get_password_hash
from sqlalchemy.future import select



class UserRepository:

    def __init__(self, session):
        self.session = session

    async def create_user(self, user_create: UserCreate):
        hashed_password = get_password_hash(user_create.password)
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            is_active=False
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str):
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def activate_user(self, user: User):
        user.is_active = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

    async def update_avatar(self, user_id: int, avatar_url: str):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            user.avatar_url = avatar_url
            await self.session.commit()
            await self.session.refresh(user)
        return user