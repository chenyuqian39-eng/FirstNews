from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
router = APIRouter(prefix="/api/favorite",tags=["favorite"])
@router.get("/check")
async def check_favorite(news_id: int = Query(...,alias="newsId"),
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)
                         ):
    is_favorited = await favorite.is_favorite(db, user.id, news_id)

    return success_response(message="favorite status checking successful",data=FavoriteCheckResponse(isFavorite=is_favorited))
@router.post("/add")
async def add_favorite(data: FavoriteAddRequest,
                       user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="successfully add collection",data = result)