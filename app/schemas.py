from __future__ import annotations

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    # Partial updates supported (only provided fields are changed)
    name: str | None = None
    description: str | None = None


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
