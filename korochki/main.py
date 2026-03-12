from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from fastapi.requests import Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from korochki.db.base import Base
from korochki.db.database import engine, get_session
from korochki.db.models import User, PaymentMethod, Application

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="korochki/templates")

@app.get("/")
async def test_connect(request: Request, db: Annotated[AsyncSession, Depends(get_session)]):
    db.execute("SELECT 1")
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