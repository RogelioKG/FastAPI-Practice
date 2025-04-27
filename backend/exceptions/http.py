from fastapi import HTTPException, status

UserNotFound_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="使用者不存在",
)

ItemNotFound_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="商品不存在",
)

IncorrectPassword_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

InvalidToken_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="無效的 Token",
    headers={"WWW-Authenticate": "Bearer"},
)

ExpiredToken_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token 已過期",
    headers={"WWW-Authenticate": "Bearer"},
)

UnauthorizedAccess_403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="無權存取資源",
)
