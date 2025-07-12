from tortoise.models import Model
from tortoise.fields import UUIDField, DatetimeField
import uuid

class BaseEntity(Model):
    ID = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    
