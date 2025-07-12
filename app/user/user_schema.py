from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TAuthTokens(BaseModel):
    access_token: str
    refresh_token: str