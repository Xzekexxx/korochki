from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional


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

    # Дополнительные поля для админ-панели
    user_login: Optional[str] = None
    user_full_name: Optional[str] = None
    user_email: Optional[str] = None
    payment_method_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    review: str = Field(min_length=1, max_length=500)


class ApplicationStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=30)
