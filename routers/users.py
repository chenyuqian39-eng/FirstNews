from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from config.db_conf import get_db
from crud import users
from utils.response import success_response
from utils.auth import get_current_user
from utils.security import verify_password
router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)): #users info db
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    # return{
    #     "code": 200,
    #     "message": "Registration succeeded",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }
    response_data =UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="User created successfully", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await users.get_user_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="Login succeeded", data=response_data)

# Get the current user from the token.
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="User info retrieved successfully", data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await users.update_user(db, user.username,user_data)
    return success_response(message="User info updated successfully", data = UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(
        password_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    res_change_pwd = await users.change_password(db, user, password_data.old_password,password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code =status.HTTP_500_INTERNAL_SERVER_ERROR, detail="fail to change password, please try again")
    return success_response(message="Password updated successfully")