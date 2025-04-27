from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Any, Literal

from jose import ExpiredSignatureError, JWTError, jwt

from config import settings
from exceptions.http import ExpiredToken_401, InvalidToken_401
from schemas.auth import TokenPair


class TokenService:
    def __init__(self):
        _settings = settings.get_settings()
        self.config: dict[str, dict[str, Any]] = {
            "access": {
                "secret": _settings.access_token_secret,
                "expire_minutes": _settings.access_token_expire_minutes,
            },
            "refresh": {
                "secret": _settings.refresh_token_secret,
                "expire_minutes": _settings.refresh_token_expire_minutes,
            },
        }

    async def generate_token(
        self, payload: dict[str, Any], *, usage: Literal["access", "refresh"]
    ) -> str:
        secret: str = self.config[usage]["secret"]
        expire_minutes: float = self.config[usage]["expire_minutes"]
        to_encode_payload = payload.copy()
        to_encode_payload.update(
            {
                "exp": datetime.now(UTC) + timedelta(minutes=expire_minutes),
                "usage": usage,  # 加入 usage 資訊
            }
        )
        return jwt.encode(to_encode_payload, secret)

    async def generate_token_pair(
        self, access_payload: dict[str, Any], refresh_payload: dict[str, Any]
    ) -> TokenPair:
        access_token = await self.generate_token(access_payload, usage="access")
        refresh_token = await self.generate_token(refresh_payload, usage="refresh")
        return TokenPair(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    async def decode_token(
        self, token: str, *, usage: Literal["access", "refresh"]
    ) -> dict[str, Any]:
        secret: str = self.config[usage]["secret"]
        try:
            payload = jwt.decode(token, secret)
            assert payload.get("usage") == usage  # 檢查 usage 資訊
            return payload
        except ExpiredSignatureError as err:
            raise ExpiredToken_401 from err  # ! 前端要負責 redirect 到 /refresh
        except JWTError as err:
            raise InvalidToken_401 from err
        except Exception as err:
            raise InvalidToken_401 from err


@lru_cache
def get_token_service() -> TokenService:
    return TokenService()
