from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.http import ItemNotFound_404, UnauthorizedAccess_403
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


class ItemCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ItemCreate, user_id: int) -> Item:
        item = Item(user_id=user_id, **data.model_dump())
        self.session.add(item)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get_all(self) -> Sequence[Item]:
        result = await self.session.execute(select(Item))
        return result.scalars().all()

    async def get_by_id_and_validate(self, item_id: int, user_id: int) -> Item:
        item = await self.session.get(Item, item_id)
        if not item:
            raise ItemNotFound_404
        elif item.user_id != user_id:
            raise UnauthorizedAccess_403
        return item

    async def get_all_by_user_id(self, user_id: int, limit: int, offset: int) -> Sequence[Item]:
        result = await self.session.execute(
            select(Item)
            .where(Item.user_id == user_id)
            .order_by(Item.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def count_by_user_id(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Item).where(Item.user_id == user_id)
        )
        return result.scalar_one()

    async def update_partial(self, item_id: int, data: ItemUpdate) -> Item:
        item = await self.session.get(Item, item_id)
        if not item:
            raise ItemNotFound_404
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        return item

    async def delete(self, item_id: int) -> None:
        item = await self.session.get(Item, item_id)
        if not item:
            raise ItemNotFound_404
        await self.session.delete(item)
