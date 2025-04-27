from collections.abc import Sequence

from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.password import hash_password
from exceptions.http import UserNotFound_404
from models.user import User
from schemas.user import UserCreate, UserUpdate


class UserCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        user.password = hash_password(data.password)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_all(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFound_404
        return user

    async def get_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise UserNotFound_404
        return user

    async def update_partial(self, user_id: int, data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return user

    async def update_password(self, user_id: int, password: SecretStr) -> User:
        user = await self.get_by_id(user_id)
        user.password = hash_password(password)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
