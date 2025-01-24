from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import db
from app.routes.categories import router as category_router
from app.routes.customers import router as customer_router
from app.routes.orders import router as order_router
from app.routes.products import router as product_router


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


app.include_router(category_router, prefix="/categories")
app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders")
app.include_router(customer_router, prefix="/customers")
