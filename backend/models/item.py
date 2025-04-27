from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, enable_repr


@enable_repr
class Item(Base):
    __tablename__ = "Item"

    # columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    brand: Mapped[str] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stock: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    # back populates
    user: Mapped["User"] = relationship(back_populates="items")  # noqa: F821, UP037 # type: ignore
