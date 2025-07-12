from tortoise.fields import (
    CharField,
    FloatField,
    JSONField,
    TextField,
    ForeignKeyRelation,
    ForeignKeyField,
    CASCADE,
)
from app.user.user_model import User
from app.base.base_entity import BaseEntity


class Product(BaseEntity):
    """
    Product model for storing product information.
    This model is used to store product details including name, description, price, and embedding.
    """

    name = CharField(max_length=120)
    description = TextField(nullable=True)
    price = FloatField()
    embedding = JSONField(nullable=True)
    user: ForeignKeyRelation[User] = ForeignKeyField(
        "models.User", related_name="products", on_delete=CASCADE
    )

    def __str__(self):
        return self.name
