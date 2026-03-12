from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from korochki.db.database import get_session
from korochki.api.schemas.application import (
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from korochki.db.models import Application, User, PaymentMethod
from korochki.core.security import get_current_admin_user
from korochki.api.schemas.user import UserResponse

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/api/admin/applications", tags=["Админ-панель: Заявки"])


@router.get("", response_model=List[ApplicationResponse])
async def get_all_applications(
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_admin_user)],
):
    stmt = (
        select(Application, User.full_name, User.login, User.email, PaymentMethod.name)
        .join(User, Application.user_id == User.id)
        .join(PaymentMethod, Application.payment_method_id == PaymentMethod.id)
        .order_by(Application.created_at.desc())
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    applications = []
    for row in rows:
        app, user_full_name, user_login, user_email, payment_method_name = row
        app_response = ApplicationResponse.model_validate(app)
        app_response.user_full_name = user_full_name
        app_response.user_login = user_login
        app_response.user_email = user_email
        app_response.payment_method_name = payment_method_name
        applications.append(app_response)
    
    return applications


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_admin_user)],
):
    application = (
        await db.execute(select(Application).where(Application.id == application_id))
    ).scalar_one_or_none()

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    allowed_statuses = ["Новая", "Идет обучение", "Обучение завершено"]
    if status_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый статус. Разрешенные: {', '.join(allowed_statuses)}",
        )

    application.status = status_data.status
    await db.commit()
    await db.refresh(application)

    return ApplicationResponse.model_validate(application)
