# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import declarative_base
# from pgvector.sqlalchemy import register_vector
# from app.core.config import get_settings

# settings = get_settings()
# engine = create_async_engine(settings.database_url.unicode_string(), echo=settings.environment == "dev")
# register_vector(engine.sync_engine)           # ensure pgvector extension is ready

# AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
# Base = declarative_base()

# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session