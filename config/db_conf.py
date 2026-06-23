from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
# Database URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:Shisheizai123@localhost:3306/news_app?charset=utf8mb4"
# Create async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, # Optional: output SQL logs
    pool_size=10, # Number of persistent connections kept in the pool
    max_overflow=20 # Number of extra connections allowed by the pool
)
# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# Dependency for getting a database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()