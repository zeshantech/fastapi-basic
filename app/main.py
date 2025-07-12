import logging
from fastapi import FastAPI
from app.ai.ai_routes import router as aiRouter
from app.auth.auth_routes import router as authRouter
from app.product.product_routes import router as productRouter
from app.core.config import get_settings
from tortoise.contrib.fastapi import register_tortoise
from app.auth.auth_middleware import AuthMiddleware
from tortoise import Tortoise, exceptions

settings = get_settings()
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

app = FastAPI(title="AI‑Shop API", version="0.1.0")

# Add authentication middleware
app.add_middleware(AuthMiddleware)

app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(productRouter, prefix="/products", tags=["products"])
app.include_router(aiRouter, prefix="/ai", tags=["ai"])

register_tortoise(
    app,
    db_url=str(settings.database_url),
    modules={"models": ["app.user.user_model", "app.product.product_model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def verify_db_connection() -> None:
    """
    Run *after* register_tortoise initialises connections.
    Succeeds quickly (SELECT 1) and prints a friendly message.
    """
    try:
        # Ping the default connection
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        logger.info("✅  Database connection established.")
    except exceptions.DBConnectionError as exc:
        # Connection object exists but is unusable
        logger.error("❌  Database ping failed: %s", exc)
        raise
    except Exception as exc:  # Covers DNS errors, refused connections, etc.
        logger.error("❌  Could not connect to database: %s", exc)
        raise


@app.on_event("shutdown")
async def log_db_shutdown() -> None:
    logger.info("ℹ️  Closing database connections…")


@app.get("/")
async def health():
    return {
        "status": "ok",
        "version": app.version,
    }
