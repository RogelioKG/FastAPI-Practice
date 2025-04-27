from fastapi import APIRouter, status

from dependencies import CurrentUserAccessDeps, UserCrudDeps
from schemas.user import UserCreate, UserRead, UserUpdate, UserUpdatePassword

router = APIRouter(tags=["users"], prefix="/api/users")


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="查詢指定使用者",
)
async def get_user_by_id(user_id: int, user_crud: UserCrudDeps):
    return await user_crud.get_by_id(user_id)


@router.get(
    "",
    response_model=list[UserRead],
    summary="取得所有使用者",
)
async def get_all_users(user_crud: UserCrudDeps):
    return await user_crud.get_all()


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    response_description="成功建立使用者",
    summary="建立使用者",
)
async def create_user(
    user_data: UserCreate,
    user_crud: UserCrudDeps,
):
    return await user_crud.create(user_data)


@router.patch(
    "/me",
    response_model=UserRead,
    summary="更新使用者資料",
)
async def update_user(
    user_data: UserUpdate,
    user_crud: UserCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    return await user_crud.update_partial(current_user.id, user_data)


@router.patch(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="更新使用者密碼",
)
async def change_password(
    password_data: UserUpdatePassword,
    user_crud: UserCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    await user_crud.update_password(current_user.id, password_data.password)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="刪除使用者",
)
async def delete_user(
    user_crud: UserCrudDeps,
    current_user: CurrentUserAccessDeps,
):
    await user_crud.delete(current_user.id)
