from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from korochki.db.database import get_session
from korochki.api.schemas.payment_method import PaymentMethodCreate, PaymentMethodResponse
from korochki.db.models import PaymentMethod
from korochki.core.security import get_current_user, get_current_admin_user
from korochki.api.schemas.user import UserResponse

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/api/payment-methods", tags=["Способы оплаты"])


@router.get("", response_model=List[PaymentMethodResponse])
async def get_payment_methods(db: AsyncSessionDep):
    payment_methods = (await db.execute(select(PaymentMethod))).scalars().all()
    return [PaymentMethodResponse.model_validate(pm) for pm in payment_methods]


@router.post("", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
async def create_payment_method(
    pm_data: PaymentMethodCreate,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_admin_user)],
):
    existing = (
        await db.execute(select(PaymentMethod).where(PaymentMethod.name == pm_data.name))
    ).scalar_one_or_none()

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Способ оплаты с таким названием уже существует",
        )

    new_payment_method = PaymentMethod(name=pm_data.name)

    db.add(new_payment_method)
    await db.commit()
    await db.refresh(new_payment_method)

    return PaymentMethodResponse.model_validate(new_payment_method)


@router.delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment_method(
    payment_method_id: int,
    db: AsyncSessionDep,
    current_user: Annotated[UserResponse, Depends(get_current_admin_user)],
):
    payment_method = (
        await db.execute(select(PaymentMethod).where(PaymentMethod.id == payment_method_id))
    ).scalar_one_or_none()

    if payment_method is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Способ оплаты не найден",
        )

    await db.delete(payment_method)
    await db.commit()

    return None
