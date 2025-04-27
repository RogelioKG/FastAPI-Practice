from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, enable_repr


@enable_repr(sensitive={"password"})
class User(Base):
    __tablename__ = "User"

    # columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)
    avatar: Mapped[str | None] = mapped_column(String(50), nullable=True)
    birthday: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # back populates
    items: Mapped[list["Item"]] = relationship(  # noqa: F821, UP037 # type: ignore
        "Item",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="Item.name",
    )
