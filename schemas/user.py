from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class UserCreate(BaseModel):
    username: str
    password: str
    gender: GenderEnum


class UserResponse(BaseModel):
    id: int
    username: str
    gender: GenderEnum
    registration_date: datetime
    ip_address: str

    class Config:
        orm_mode = True


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
