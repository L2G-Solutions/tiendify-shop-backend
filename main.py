from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import db
from app.routes.auth.private_routes import router as private_auth_router
from app.routes.auth.public_routes import router as public_auth_router
from app.routes.auth.secret_keys import router as secret_key_router
from app.routes.categories import router as category_router
from app.routes.customers import router as customer_router
from app.routes.orders import router as order_router
from app.routes.products import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Controls the lifespan of the application. Initializes and closes the database connection.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
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


app.include_router(public_auth_router, prefix="/auth/public")
app.include_router(private_auth_router, prefix="/auth/private")
app.include_router(secret_key_router, prefix="/auth/private/secret-keys")

app.include_router(category_router, prefix="/categories")
app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders")
app.include_router(customer_router, prefix="/customers")
