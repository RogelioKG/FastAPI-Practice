from pydantic import BaseModel


class Pagination[T](BaseModel):
    total: int
    page: int
    page_size: int
    items: list[T]
