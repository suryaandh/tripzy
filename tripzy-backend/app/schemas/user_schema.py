from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class MeResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True