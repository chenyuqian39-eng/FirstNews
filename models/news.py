from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Text, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="Created time"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="Updated time"
    )

class Category(Base):
    __tablename__ = "news_category"#Table name
    id : Mapped[int] =mapped_column(Integer, primary_key=True,autoincrement=True)
    name : Mapped[str] = mapped_column(String(50), unique=True,nullable=False,comment="Category name")
    sort_order: Mapped[int] = mapped_column(Integer, default=0,nullable=False, comment = "Sort order")
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

class News(Base):
    __tablename__ = "news"
# Create indexes to improve query performance
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'), #category id high frequency query
        Index('idx_publish_time', 'publish_time')# Sort by publish time
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement = True, comment = "News ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment = "News title")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment = "News summary")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="News content")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="Cover image URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="Author")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="Category ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False,comment="View count")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment = "Publish time")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"