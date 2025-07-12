from pydantic import BaseModel
from uuid import UUID

class TCurrentUser(BaseModel):
    ID: UUID
    email: str
