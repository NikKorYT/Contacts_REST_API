from fastapi import FastAPI
from schemes import Contact

app = FastAPI()

@app.get("/ping")
async def pong():
    return {"message": "pong!"}

@app.post("/contact")
async def create_contact(contact: Contact):
    return {"first_name": contact.name, "last_name": contact.surname, "email": contact.email, "phone": contact.phone, "date_of_birth": contact.date_of_birth, "additional_info": contact.additional_info}