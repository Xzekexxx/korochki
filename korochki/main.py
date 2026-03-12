from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from korochki.db.base import Base
from korochki.db.database import engine, get_session
from korochki.db.models import User, PaymentMethod, Application
from korochki.api.endpoints import auth, applications, payment_methods

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(payment_methods.router)

templates = Jinja2Templates(directory="korochki/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("registr.html", {"request": request})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/test-db")
async def test_connect(request: Request, db: Annotated[AsyncSession, Depends(get_session)]):
    await db.execute(select(1))
    db_connected = True

    users = (await db.execute(select(User))).scalars().all()

    return templates.TemplateResponse(
        "db_connect.html",
        {
            "request": request,
            "db_connected": db_connected,
            "users": users,
        },
    )
