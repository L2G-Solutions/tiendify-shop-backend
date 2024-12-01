from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print("Connected to database")
    yield
    await db.disconnect()


app = FastAPI()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def handle_get_health():
    return {"status": "ok"}
