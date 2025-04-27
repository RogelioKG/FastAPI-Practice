from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class UserType:
    Id = Annotated[
        int,
        Field(
            json_schema_extra={
                "title": "Id",
                "description": "使用者唯一 Id",
                "examples": [1],
            }
        ),
    ]
    Name = Annotated[
        str,
        Field(
            json_schema_extra={
                "title": "Name",
                "description": "使用者姓名",
                "examples": ["RogelioKG"],
            }
        ),
    ]
    Email = Annotated[
        EmailStr,
        Field(
            json_schema_extra={
                "title": "Email",
                "description": "使用者電子郵件",
                "examples": ["user@example.com"],
            }
        ),
    ]
    Avatar = Annotated[
        str,
        Field(
            json_schema_extra={
                "title": "Avatar",
                "description": "使用者頭像圖片網址",
                "examples": ["https://example.com/avatar.jpg"],
            }
        ),
    ]
    Password = Annotated[
        SecretStr,
        Field(
            min_length=6,
            json_schema_extra={
                "title": "Password",
                "description": "使用者登入密碼，至少 6 個字元",
                "examples": ["securePass123"],
            },
        ),
    ]
    Age = Annotated[
        int,
        Field(
            gt=0,
            lt=100,
            json_schema_extra={
                "title": "Age",
                "description": "使用者年齡，需介於 1 到 99 歲",
                "examples": [25],
            },
        ),
    ]
    Birthday = Annotated[
        date,
        Field(
            json_schema_extra={
                "title": "Birthday",
                "description": "使用者生日（格式 YYYY-MM-DD）",
                "examples": ["1998-08-08"],
            },
        ),
    ]


class UserCreate(BaseModel):
    name: UserType.Name
    email: UserType.Email
    avatar: UserType.Avatar | None = None
    password: UserType.Password
    age: UserType.Age
    birthday: UserType.Birthday

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: UserType.Id
    name: UserType.Name
    email: UserType.Email
    avatar: UserType.Avatar | None = None
    age: UserType.Age
    birthday: UserType.Birthday

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: UserType.Name | None = None
    email: UserType.Email | None = None
    avatar: UserType.Avatar | None = None
    age: UserType.Age | None = None
    birthday: UserType.Birthday | None = None


class UserUpdatePassword(BaseModel):
    password: UserType.Password
