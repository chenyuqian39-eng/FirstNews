from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

#查询数据库执行
async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
async def get_news_list(db: AsyncSession, category_id, skip: int = 0, limit: int = 10):
    #查询的是制定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()