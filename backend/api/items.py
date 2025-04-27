from fastapi import APIRouter, status

from dependencies import CurrentUserAccessDeps, ItemCrudDeps
from schemas.item import ItemCreate, ItemRead, ItemUpdate
from schemas.misc import Pagination

router = APIRouter(tags=["items"], prefix="/api/items")


@router.get(
    "",
    response_model=Pagination[ItemRead],
    summary="取得使用者的所有商品 (分頁)",
)
async def get_user_all_items(
    item_crud: ItemCrudDeps,
    current_user: CurrentUserAccessDeps,
    page: int = 1,
    page_size: int = 20,
):
    offset = (page - 1) * page_size
    items = await item_crud.get_all_by_user_id(current_user.id, limit=page_size, offset=offset)
    total = await item_crud.count_by_user_id(current_user.id)
    return Pagination[ItemRead](
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get(
    "/{item_id}",
    response_model=ItemRead,
    summary="取得使用者的指定商品",
)
async def get_user_item(
    item_id: int,
    item_crud: ItemCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    return await item_crud.get_by_id_and_validate(item_id, current_user.id)


@router.post(
    "",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
    response_description="成功建立使用者的商品",
    summary="建立使用者的商品",
)
async def create_user_item(
    item_data: ItemCreate,
    item_crud: ItemCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    return await item_crud.create(item_data, current_user.id)


@router.patch(
    "/{item_id}",
    response_model=ItemRead,
    summary="更新使用者的商品",
)
async def update_user_item(
    item_id: int,
    item_data: ItemUpdate,
    item_crud: ItemCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    await item_crud.get_by_id_and_validate(item_id, current_user.id)
    return await item_crud.update_partial(item_id, item_data)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="刪除使用者的商品",
)
async def delete_user_item(
    item_id: int,
    item_crud: ItemCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    await item_crud.get_by_id_and_validate(item_id, current_user.id)
    await item_crud.delete(item_id)
