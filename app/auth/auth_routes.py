from fastapi import APIRouter
from app.user.user_schema import UserCreate, UserLogin, TAuthTokens
from app.auth.auth_service import AuthService

router = APIRouter()
authService = AuthService()


@router.post("/register", response_model=TAuthTokens)
async def register(input: UserCreate):
    return await authService.register(input)

@router.post("/login", response_model=TAuthTokens)
async def login(input: UserLogin):
    return await authService.login(input)