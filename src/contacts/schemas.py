from pydantic import BaseModel, EmailStr
from datetime import date


class Contact(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: int
    date_of_birth: date
    additional_info: str | None = None


class ContactResponse(Contact):
    id: int

    class Config:
        from_attributes = True


class ContactCreate(Contact):
    pass


class ContactUpdate(Contact):
    pass


class ContactDelete(Contact):
    pass
