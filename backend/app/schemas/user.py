from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserRegister(BaseModel):
    email:     EmailStr
    password:  str
    full_name: str
    role:      UserRole

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserResponse(BaseModel):
    id:          int
    email:       str
    full_name:   str
    role:        UserRole
    is_verified: bool
    created_at:  datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:   str
    user:         UserResponse

class TokenData(BaseModel):
    user_id:  Optional[int] = None
    role:     Optional[str] = None