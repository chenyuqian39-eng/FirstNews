
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import get_current_user
from models.users import User
from config.db_conf import get_db
from utils.response import success_response
from schemas.history import HistoryAddRequest
from crud import history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(data: HistoryAddRequest,
                       user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    result = await history.add_news_history(db, user.id, data.news_id)
    return success_response(message="successfully added history", data=result)


@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    rows, total = await history.get_history_list(db, user.id, page, page_size)
    history_list = [
        {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "categoryId": news.category_id,
            "views": news.views,
            "publishTime": news.publish_time,
            "viewTime": view_time,
            "historyId": history_id,
        }
        for news, view_time, history_id in rows
    ]

    return success_response(
        message="successfully got history list",
        data={
            "list": history_list,
            "total": total,
            "hasMore": total > page * page_size,
        },
    )


@router.delete("/delete/{news_id}")
async def delete_history(
        news_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    deleted = await history.remove_news_history(db, user.id, news_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="History record not found")
    return success_response(message="successfully deleted history")


@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    deleted_count = await history.remove_all_history(db, user.id)
    return success_response(
        message="successfully cleared history",
        data={"deletedCount": deleted_count},
    )
