from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime, date
from typing import Optional
import re


class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=10, max_length=20)
    email: EmailStr
    role: str = Field(default="user")

    @field_validator('login')
    @classmethod
    def validate_login(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Логин должен содержать только латиницу и цифры')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r'^\(\d{3}\)\d{3}-\d{2}-\d{2}$', v):
            raise ValueError('Телефон должен быть в формате (XXX)XXX-XX-XX')
        return v


class UserLogin(BaseModel):
    login: str = Field(description="Логин пользователя")
    password: str = Field(description="Пароль пользователя")


class UserResponse(BaseModel):
    id: int
    login: str
    full_name: str
    phone: str
    email: str
    role: str = "user"

    model_config = ConfigDict(from_attributes=True)


class PaymentMethodCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PaymentMethodResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    course_name: str = Field(min_length=1, max_length=200)
    desired_start_date: date
    payment_method_id: int


class ApplicationUpdate(BaseModel):
    course_name: Optional[str] = Field(None, min_length=1, max_length=200)
    desired_start_date: Optional[date] = None
    payment_method_id: Optional[int] = None
    status: Optional[str] = None
    review: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    course_name: str
    desired_start_date: date
    payment_method_id: int
    status: str
    created_at: datetime
    review: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)