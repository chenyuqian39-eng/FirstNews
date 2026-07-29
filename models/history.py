
from datetime import datetime

from sqlalchemy import (
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
    DateTime,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.news import News
from models.users import User
class Base(DeclarativeBase):
    pass


class History(Base):
    """
    收藏表 ORM 模型
    """

    __tablename__ = "history"

    # 创建索引
    __table_args__ = (
        #uniqueConstraint 唯一约束； 当前用户只能收藏一次
        UniqueConstraint(
            "user_id",
            "news_id",
            name="user_news_unique",
        ),
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="history ID",
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
        comment="user ID",
    )

    news_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(News.id),
        nullable=False,
        comment="news ID",
    )

    view_time: Mapped[datetime] = mapped_column(
        "view_time",
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="history view time",
    )

    def __repr__(self):
        return (
            f"<History(id={self.id}, "
            f"user_id={self.user_id}, "
            f"news_id={self.news_id}, "
            f"view_time={self.view_time})>"
        )
