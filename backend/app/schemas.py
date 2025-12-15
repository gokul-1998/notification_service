from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None

class NotificationCreate(BaseModel):
    title: str
    message: str

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    created_by: int
    created_at: datetime
    is_read: bool
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class NotificationStatusUpdate(BaseModel):
    is_read: bool
