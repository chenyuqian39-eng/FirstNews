from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, select
from models.history import History
from models.news import News

async def add_news_history(
        db:AsyncSession,
        user_id: int,
        news_id: int
):
    query = select(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(query)
    his = result.scalar_one_or_none()

    if his:
        his.view_time = datetime.utcnow()
    else:
        his = History(user_id=user_id, news_id=news_id)
        db.add(his)

    await db.commit()
    await db.refresh(his)
    return his


async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10,
):
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    query = (
        select(
            News,
            History.view_time.label("view_time"),
            History.id.label("history_id"),
        )
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


async def remove_news_history(
        db: AsyncSession,
        user_id: int,
        news_id: int,
):
    stmt = delete(History).where(
        History.user_id == user_id,
        History.news_id == news_id,
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def remove_all_history(
        db: AsyncSession,
        user_id: int,
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
