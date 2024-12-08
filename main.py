from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from src.contacts.router import router as contacts_router
from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Redis connection
    redis_instance = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_instance)
    yield
    # Cleanup (if needed)
    await redis_instance.close()

app = FastAPI(lifespan=lifespan)

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def pong():
    return {"message": "pong!"}
