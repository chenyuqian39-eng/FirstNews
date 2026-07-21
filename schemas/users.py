from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_bcrypt_password_length(cls, value: str):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return value


class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="Nickname")
    avatar: Optional[str] = Field(None, max_length=255, description="Avatar URL")
    gender: Optional[str] = Field(None, max_length=10, description="Gender")
    bio: Optional[str] = Field(None, max_length=500, description="Bio")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="Old password")
    new_password: str = Field(..., min_length=6, alias = "newPassword", description="New password")
