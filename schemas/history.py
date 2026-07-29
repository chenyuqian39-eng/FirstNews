from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class HistoryCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isHistory")

class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")