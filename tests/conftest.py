import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import pytest
from sqlalchemy.orm import sessionmaker
from config.db import Base, get_db
from main import app

from config.general import settings
from src.auth.models import User
from src.auth.pass_utils import get_password_hash
from src.auth.utils import create_access_token, create_refresh_token
from src.contacts.models import Contact

DATABASE_URL = settings.database_test_url

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db(setup_database):
    async with AsyncSessionLocal() as session:
        yield session
    app.dependency_overrides[get_db] = get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def user_password(faker):
    return faker.password()


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session, faker, user_password):
    hased_password = get_password_hash(user_password)
    user = User(
        email=faker.email(),
        username=faker.user_name(),
        hashed_password=hased_password,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def auth_headers(test_user: User):
    access_token = create_access_token(data={"sub": test_user.username})
    refresh_token = create_refresh_token(data={"sub": test_user.username})
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Refresh-Token": f"{refresh_token}",
    }
    return headers


@pytest.fixture(scope="function")
async def test_user_contact(db_session, faker, test_user):
    contact = Contact(
        name=faker.first_name(),
        surname=faker.last_name(),
        email=faker.email(),
        phone=faker.random_int(min=100000000, max=999999999),
        date_of_birth=faker.date_of_birth(),
        additional_info=faker.text(),
        owner_id=test_user.id,
    )
    db_session.add(contact)
    await db_session.commit()
    await db_session.refresh(contact)
    return contact
