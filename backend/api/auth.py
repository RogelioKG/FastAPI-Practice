from fastapi import APIRouter

from auth.password import verify_password
from dependencies import CurrentUserRefreshDeps, TokenServiceDeps, UserCrudDeps
from exceptions.http import IncorrectPassword_401
from schemas.auth import LoginForm, TokenPair

router = APIRouter(
    tags=["auth"],
    prefix="/api/auth",
)


@router.post(
    "/login",
    response_model=TokenPair,
    summary="使用者登入",
)
async def login(
    form_data: LoginForm,
    user_crud: UserCrudDeps,
    token_service: TokenServiceDeps,
):
    user = await user_crud.get_by_email(form_data.username)
    if not verify_password(form_data.password, user.password):
        raise IncorrectPassword_401

    token_pair = await token_service.generate_token_pair(
        {"id": user.id},
        {"id": user.id},
    )

    return token_pair


@router.post(
    "/refresh",
    response_model=TokenPair,
    summary="刷新 token",
)
async def refresh(
    token_service: TokenServiceDeps,
    current_user: CurrentUserRefreshDeps,
):
    token_pair = await token_service.generate_token_pair(
        {"id": current_user.id},
        {"id": current_user.id},
    )

    return token_pair
