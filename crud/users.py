# search db by username
import uuid

from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils import security
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest


#search db by username
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#create user
async def create_user(db: AsyncSession, user_data: UserRequest):
    # Encrypt the password first -> add
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #rereda newest user from db
    return user

# generate token
async def create_token(db: AsyncSession, user_id: int):
    #generate +expire date  -> check if the current user have token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)

    await db.commit()
    return token


async def get_user_by_token(db: AsyncSession, token: str):
    query = (
        select(User)
        .join(UserToken, UserToken.user_id == User.id)
        .where(
            UserToken.token == token,
            UserToken.expires_at > datetime.now()
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    #没有设置值的不更新
    query = update(User).where(User.username == username).values(user_data.model_dump(
        exclude_unset = True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()
    # check update
    if result.rowcount ==0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await get_user_by_username(db, username)
    return updated_user

#change psw : auth old psw- new psw encry - change
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False
    hashed_new_password = security.get_hash_password(new_password)
    user.password = hashed_new_password
    # sqlalchemy handle this user obj, make sure to commit, avoid session expire or closed (can't submit)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True