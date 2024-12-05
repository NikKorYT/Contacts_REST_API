from fastapi import FastAPI, Path
from src.contacts.router import router
from src.auth.router import router

app = FastAPI()

app.include_router(router, prefix="/contacts", tags=["contacts"])
app.include_router(router, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def pong():
    return {"message": "pong!"}
