from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

#规划两个类：一个新闻模型类 +收藏的模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id:int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
#收藏列表接口响应模型类
class FavoriteListRequest(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(..., alias="hasMore")
#ORM对象中提取值 别名和字段名要兼容
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )