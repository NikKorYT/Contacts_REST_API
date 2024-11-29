from pydantic import BaseModel, EmailStr
from datetime import date

class Contact(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: int
    date_of_birth: date
    additional_info: str|None = None