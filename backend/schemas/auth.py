from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# 自動從 request 的 authorization header 拿取 bearer token
OAuth2Token = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="api/auth/login"))]
# 自動從 request 抓取登入資訊 (username 與 password 欄位，此為 OAuth 2.0 規定)
LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
