from fastapi import APIRouter

from config.settings import get_settings

router = APIRouter(tags=["config"], prefix="/api/config")


@router.get(
    "",
    summary="取得設定",
)
async def get_config():
    return get_settings().to_dict()  # ! 測試用，prod env 不能這樣搞
