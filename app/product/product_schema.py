from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    ID: UUID
    embedding: list[float] | None = Field(default=None, exclude=True)
    
    model_config = ConfigDict(
        from_attributes=True,
    )

class ProductReadFull(ProductRead):
    embedding: list[float] | None = Field(default=None, exclude=False)