import os
from dataclasses import asdict, dataclass
from functools import lru_cache


def try_getenv(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set.")
    return value


@dataclass
class Settings:
    app_mode: str
    port: int
    reload: bool
    database_uri: str
    access_token_secret: str
    access_token_expire_minutes: float
    refresh_token_secret: str
    refresh_token_expire_minutes: float
    app_name: str = "TestFastAPI"
    author: str = "RogelioKG"

    @classmethod
    def from_env(cls):
        return cls(
            app_mode=try_getenv("APP_MODE"),
            port=int(try_getenv("PORT")),
            reload=try_getenv("RELOAD").lower() == "true",
            database_uri=try_getenv("DATABASE_URI"),
            access_token_secret=try_getenv("ACCESS_TOKEN_SECRET"),
            access_token_expire_minutes=float(try_getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
            refresh_token_secret=try_getenv("REFRESH_TOKEN_SECRET"),
            refresh_token_expire_minutes=float(try_getenv("REFRESH_TOKEN_EXPIRE_MINUTES")),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@lru_cache
def get_settings():
    return Settings.from_env()
