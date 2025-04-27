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
    """自動為每個 SQLAlchemy Model 提供 `__repr__` 方法，並屏蔽敏感欄位

    Example
    -------
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
