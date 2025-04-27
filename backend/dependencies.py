from collections.abc import AsyncGenerator
from typing import Annotated, Any, Literal

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import TokenService, get_token_service
from crud.item import ItemCrud
from crud.user import UserCrud
from database.session import AsyncSessionLocal
from exceptions.http import InvalidToken_401, UnauthorizedAccess_403
from models.user import User
from schemas.auth import OAuth2Token


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def get_user_crud(session: Annotated[AsyncSession, Depends(get_session)]) -> UserCrud:
    return UserCrud(session)


async def get_item_crud(session: Annotated[AsyncSession, Depends(get_session)]) -> ItemCrud:
    return ItemCrud(session)


def get_current_user_with_token(*, usage: Literal["access", "refresh"]):
    async def wrapper(
        token: OAuth2Token,
        user_crud: Annotated[UserCrud, Depends(get_user_crud)],
        token_service: Annotated[TokenService, Depends(get_token_service)],
    ) -> User:
        payload = await token_service.decode_token(token, usage=usage)
        user_id: int | None = payload.get("id")
        if user_id is None:
            raise InvalidToken_401
        return await user_crud.get_by_id(user_id)

    return wrapper


async def verify_user_ownership(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user_with_token(usage="access"))],
):
    if user_id != current_user.id:
        raise UnauthorizedAccess_403


SessionDeps = Annotated[AsyncSession, Depends(get_session)]
UserCrudDeps = Annotated[UserCrud, Depends(get_user_crud)]
ItemCrudDeps = Annotated[ItemCrud, Depends(get_item_crud)]
TokenServiceDeps = Annotated[TokenService, Depends(get_token_service)]
CurrentUserAccessDeps = Annotated[User, Depends(get_current_user_with_token(usage="access"))]
CurrentUserRefreshDeps = Annotated[User, Depends(get_current_user_with_token(usage="refresh"))]
