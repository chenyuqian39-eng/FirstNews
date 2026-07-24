from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func

from models.favorite import Favorite
from models.news import News


#check status: if current user collect this news
async def is_favorite(
        db:AsyncSession,
        user_id: int,
        news_id: int ):
    query = select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id == news_id)
    result =await db.execute(query)
    # if have collection or not
    return result.scalar_one_or_none() is not None

async def add_news_favorite(
        db:AsyncSession,
        user_id: int,
        news_id: int,
):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(
        db:AsyncSession,
        user_id: int,
        news_id: int
):
    stmt = delete(Favorite).where(Favorite.user_id==user_id, Favorite.news_id==news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0
#get collection list( user +page )
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10):
    # 总量+收藏的新闻列表
    count_query = select(func.count()).where(Favorite.user_id==user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    #获取收藏列表 联表查询join() + 收藏时间排序+分页
    #select(查询主体模型类,字段别名).join(联合查询的模型类，联合查询的条件).where().order_by().offset().limit()
    #字段别名： 模型类.字段.别名
    offset = (page - 1) * page_size
    query = (select(News, Favorite.created_at.lable("favorite_time"), Favorite.id.lable("favorite_id"))
             .join(Favorite, Favorite.news_id==News.id)
             .where(Favorite.user_id ==user_id)
             .order_by(Favorite.created_at.desc())
             .offset(offset).limit(page_size))
#[
#   (新闻对象，收藏时间，收藏id)
#]
    result = await db.execute(query)
    rows = result.all()
    return rows, total