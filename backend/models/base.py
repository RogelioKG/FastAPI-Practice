from collections.abc import Callable
from typing import overload

from sqlalchemy.orm import DeclarativeBase, class_mapper


class Base(DeclarativeBase):
    pass


@overload
def enable_repr[T](
    cls: None,
    *,
    sensitive: set[str] | None = None,
) -> Callable[[type[T]], type[T]]: ...


@overload
def enable_repr[T](
    cls: type[T],
    *,
    sensitive: set[str] | None = None,
) -> type[T]: ...


def enable_repr[T](
    cls: type[T] | None = None,
    *,
    sensitive: set[str] | None = None,
) -> Callable[[type[T]], type[T]] | type[T]:
    """為 SQLAlchemy Model 提供自動生成的 `__repr__` 方法，並可選擇性地屏蔽敏感欄位。

    此裝飾器會自動為 SQLAlchemy Model 類別生成一個 `__repr__` 方法，
    該方法會顯示所有欄位的值，但會將指定的敏感欄位值替換為 "***"。

    Parameters
    ----------
    cls : type[T] | None, optional
        要裝飾的類別。如果為 None，則返回一個裝飾器函數。
    sensitive : set[str] | None, optional
        需要被屏蔽的敏感欄位名稱集合。如果為 None，則使用空集合。

    Returns
    -------
    Callable[[type[T]], type[T]] | type[T]
        如果 cls 為 None，返回裝飾器函數；否則返回裝飾後的類別。

    Examples
    --------
    >>> @enable_repr(sensitive={"password", "email"})
    ... class User(Base):
    ...     __tablename__ = "User"
    ...     id = mapped_column(Integer, primary_key=True)
    ...     username = mapped_column(String(50))
    ...     email = mapped_column(String(100))
    ...     password = mapped_column(String(100))
    >>> user = User(id=1, username="john", email="john@example.com", password="123")
    >>> print(user)
    User(id=1, username='john', email=***, password=***)
    """

    if sensitive is None:
        sensitive = set()

    def wrapper(cls_: type[T]) -> type[T]:
        setattr(cls_, "_sensitive", sensitive)  # noqa: B010

        def __repr__(self) -> str:
            columns = class_mapper(self.__class__).columns.keys()
            repr_dict = {}
            for col in columns:
                value = getattr(self, col)
                if col in self.__class__._sensitive:
                    repr_dict[col] = "***"
                else:
                    repr_dict[col] = repr(value)
            repr_data = ", ".join(f"{k}={v}" for k, v in repr_dict.items())
            return f"{self.__class__.__name__}({repr_data})"

        cls_.__repr__ = __repr__
        return cls_

    return wrapper if cls is None else wrapper(cls)
