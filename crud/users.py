# search db by username
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()