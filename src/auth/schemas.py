from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserResponse(UserBase):
    id: int
    
    class Config:
        from_atriibutes = True
            
class UserCreate(UserBase):
    password: str
    
class TokenData(BaseModel):
    username: str | None = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str