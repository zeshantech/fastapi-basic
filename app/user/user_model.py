from tortoise.fields import CharField
from app.base.base_entity import BaseEntity

class User(BaseEntity):
    """User model for storing user information.
    This model is used to store user details including email, hashed password, and full name.
    """

    email = CharField(max_length=320, unique=True, nullable=False)
    password = CharField(max_length=128, nullable=False)
    full_name = CharField(max_length=120, nullable=True)


    def __str__(self):
        return self.email