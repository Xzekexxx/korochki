from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from korochki.db.database import get_session
from korochki.api.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ReviewCreate,
)
from korochki.db.models import Application, User
from korochki.core.security import get_current_user, get_current_admin_user
from korochki.api.schemas.user import UserResponse

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/api/applications", tags=["Заявки"])


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    app_data: ApplicationCreate,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    new_application = Application(
        user_id=current_user.id,
        course_name=app_data.course_name,
        desired_start_date=app_data.desired_start_date,
        payment_method_id=app_data.payment_method_id,
        status="Новая",
    )

    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    return ApplicationResponse.model_validate(new_application)


@router.get("", response_model=List[ApplicationResponse])
async def get_user_applications(
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    applications = (
        await db.execute(
            select(Application).where(Application.user_id == current_user.id)
        )
    ).scalars().all()

    result = []
    for app in applications:
        app_dict = ApplicationResponse.model_validate(app)

        result.append(app_dict)
    
    return result


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):

    application = (
        await db.execute(select(Application).where(Application.id == application_id))
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    if application.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заявке",
        )

    return ApplicationResponse.model_validate(application)


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    app_data: ApplicationUpdate,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):

    application = (
        await db.execute(select(Application).where(Application.id == application_id))
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    if application.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заявке",
        )

    update_data = app_data.model_dump(exclude_unset=True)
    
    if current_user.role != "admin":
        update_data.pop("status", None)
        update_data.pop("review", None)

    for field, value in update_data.items():
        if value is not None:
            setattr(application, field, value)

    await db.commit()
    await db.refresh(application)

    return ApplicationResponse.model_validate(application)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: int,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):

    application = (
        await db.execute(select(Application).where(Application.id == application_id))
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    if application.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заявке",
        )

    await db.delete(application)
    await db.commit()

    return None


@router.post("/{application_id}/review", response_model=ApplicationResponse)
async def add_review(
    application_id: int,
    review_data: ReviewCreate,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):

    application = (
        await db.execute(select(Application).where(Application.id == application_id))
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заявке",
        )

    if application.status != "Обучение завершено":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отзыв можно оставить только после завершения обучения",
        )

    if application.review and application.review.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отзыв уже оставлен",
        )

    application.review = review_data.review
    await db.commit()
    await db.refresh(application)

    return ApplicationResponse.model_validate(application)
