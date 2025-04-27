from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ItemType:
    Id = Annotated[
        int,
        Field(
            json_schema_extra={
                "title": "Id",
                "description": "商品唯一 Id",
                "examples": [1],
            },
        ),
    ]
    Name = Annotated[
        str,
        Field(
            json_schema_extra={
                "title": "Name",
                "description": "商品名稱",
                "examples": ["筆記型電腦"],
            },
        ),
    ]
    Price = Annotated[
        float,
        Field(
            gt=0,
            json_schema_extra={
                "title": "Price",
                "description": "商品價格，需大於 0",
                "examples": [29999.0],
            },
        ),
    ]
    Brand = Annotated[
        str,
        Field(
            json_schema_extra={
                "title": "Brand",
                "description": "商品品牌",
                "examples": ["ASUS"],
            },
        ),
    ]
    Description = Annotated[
        str,
        Field(
            json_schema_extra={
                "title": "Description",
                "description": "商品描述",
                "examples": ["高效能筆記型電腦，適合工作與遊戲"],
            }
        ),
    ]
    Stock = Annotated[
        int,
        Field(
            ge=0,
            json_schema_extra={
                "title": "Stock",
                "description": "商品庫存數量，需大於等於 0",
                "examples": [10],
            },
        ),
    ]


class ItemCreate(BaseModel):
    name: ItemType.Name
    price: ItemType.Price
    brand: ItemType.Brand
    description: ItemType.Description | None = None
    stock: ItemType.Stock = 0

    model_config = ConfigDict(from_attributes=True)


class ItemRead(BaseModel):
    id: ItemType.Id
    name: ItemType.Name
    price: ItemType.Price
    brand: ItemType.Brand
    description: ItemType.Description
    stock: ItemType.Stock

    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    name: ItemType.Name | None = None
    price: ItemType.Price | None = None
    brand: ItemType.Brand | None = None
    description: ItemType.Description | None = None
    stock: ItemType.Stock | None = None
