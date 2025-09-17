from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Base User schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    name: str


# Schema for creating a new user
class UserCreate(UserBase):
    password: str


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for updating user information
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    
class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str


# Schema for user response (what gets returned to client)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    api_request_count: int
    
    class Config:
        from_attributes = True


# Schema for user response without sensitive API usage data
class UserPublic(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    id : Optional[int] = None


# Schema for API usage tracking
class UserApiUsage(BaseModel):
    user_id: int
    api_request_count: int
    email: str
    name: str
    
    class Config:
        from_attributes = True
