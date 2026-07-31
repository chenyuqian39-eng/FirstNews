from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from cache.news_cache import (
    get_cached_categories,
    get_news_list as get_cached_news_list,
    set_cache_news_list,
    set_news_categories,
)
from models.news import Category, News

logger = logging.getLogger(__name__)

#Execute database query
async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    logger.info("Start getting news categories")
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    logger.info("Cached categories: %s", cached_categories)
    if cached_categories:
        logger.info("Redis cache hit: news categories")
        return cached_categories

    logger.info("Redis cache miss: news categories, loading from database")
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories =  result.scalars().all() #ORM
#写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        cache_saved = await set_news_categories(categories)
        logger.info("Redis cache save categories result: %s", cache_saved)
#返回数据
    return categories


#Get news details
async def get_news_list(db: AsyncSession, category_id, skip: int = 0, limit: int = 10):
    #await get_cached_categories(category_id,页码,limit)
    #skip =(页码-1）*每页数量 -页码 =skip//每页数量 +1   整除 无小数
    page = skip// limit +1
    cached_list = await get_cached_news_list(category_id, page, limit)
    if cached_list:
        logger.info(
            "Redis cache hit: news list category_id=%s page=%s page_size=%s",
            category_id,
            page,
            limit,
        )
        return cached_list

    logger.info(
        "Redis cache miss: news list category_id=%s page=%s page_size=%s",
        category_id,
        page,
        limit,
    )
    #Query all news under the specified category
    stmt = (
        select(News)
        .where(News.category_id == category_id)
        .order_by(News.publish_time.desc(), News.id.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    news_list = result.scalars().all()
    # write in cache
    if news_list:
        news_data = [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "image": item.image,
                "author": item.author,
                "categoryId": item.category_id,
                "views": item.views,
                "publishTime": item.publish_time,
            }
            for item in news_list
        ]
        cache_saved = await set_cache_news_list(
            category_id,
            page,
            limit,
            jsonable_encoder(news_data),
        )
        logger.info("Redis cache save news list result: %s", cache_saved)
        return news_data
    return []



async def increase_news_count(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit() #Commit immediately instead of waiting for the session dependency commit
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, category_id: int, news_id: int, limit: int=5):
    #ORDERBY view & publish time
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.id.desc(),
        News.publish_time.desc()

    ).limit(limit)
    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()
    #列表推导式 推导出新闻的核心数据，然后再return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views
    } for news_detail in related_news]
