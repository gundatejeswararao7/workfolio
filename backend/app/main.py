from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, SessionLocal, engine
from .routers import ai, auth, chat, feed, notifications, users, works


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Loopline API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(feed.router)
app.include_router(works.router)
app.include_router(notifications.router)
app.include_router(chat.router)
app.include_router(ai.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "loopline-api"}