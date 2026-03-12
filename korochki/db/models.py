from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import datetime, date

from korochki.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default="user")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    applications: Mapped[list["Application"]] = relationship(back_populates="user")

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="payment_method")

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    course_name: Mapped[str] = mapped_column(nullable=False)
    desired_start_date: Mapped[date] = mapped_column(nullable=False)
    payment_method_id: Mapped[int] =  mapped_column(ForeignKey('payment_methods.id'))
    status: Mapped[str] = mapped_column(nullable=False, default="Новая")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    review: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="applications")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="applications")