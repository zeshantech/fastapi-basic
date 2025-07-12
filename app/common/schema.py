from pydantic import BaseModel
from uuid import UUID

class CommonParams(BaseModel):
    ID: UUID

class MessageOutput(BaseModel):
    message: str