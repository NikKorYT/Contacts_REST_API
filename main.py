from fastapi import FastAPI, Path
from src.contacts.router import router as contacts_router
from src.auth.router import router as auth_router

app = FastAPI()

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def pong():
    return {"message": "pong!"}
