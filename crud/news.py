from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

#Execute database query
async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
#Get news details
async def get_news_list(db: AsyncSession, category_id, skip: int = 0, limit: int = 10):
    #Query all news under the specified category
    stmt = select(func.count(News.id)).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalar_one() #Only one result is expected; otherwise an error is raised

# Get news details
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_count(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    await db.execute(stmt)
    await db.commit() #Commit immediately instead of waiting for the session dependency commit
