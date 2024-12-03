from pydantic import BaseModel, EmailStr
from datetime import date

class Contact(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: int
    date_of_birth: date
    additional_info: str|None = None
    
class ContactResponse(Contact):
    id: int
    
    class Config:
        from_atributes = True
        
class ContactCreate(BaseModel):
    pass

class ContactUpdate(BaseModel):
    pass