from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

#查询数据库执行
async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
#获取新闻详情
async def get_news_list(db: AsyncSession, category_id, skip: int = 0, limit: int = 10):
    #查询的是制定分类下的所有新闻
    stmt = select(func.count(News.id)).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalar_one() #只能有一个结果，否则报错

# 获取新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_count(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    await db.execute(stmt)
    await db.commit() #dbconf中的commit是所有数据更新完后再更新 这个直接更新写入
