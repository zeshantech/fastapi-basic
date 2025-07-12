from app.user.user_service import UserService
from app.user.user_schema import UserCreate, TAuthTokens, UserLogin
from app.core.token_service import TokenService
from app.common.utils import check_password
from app.common.exceptions import UnauthorizedException


class AuthService:
    def __init__(
        self,
    ):
        self.userService = UserService()
        self.tokenService = TokenService()

    async def register(self, data: UserCreate):
        existing_user = await self.userService.find_user_by_email(data.email)
        if existing_user:
            raise UnauthorizedException("Email already registered")

        user = await self.userService.create_user(data)
        tokens = await self.tokenService.assign_auth_tokens(user)

        return tokens

    async def login(self, input: UserLogin) -> TAuthTokens:
        user = await self.userService.find_user_by_email(input.email)
        if not user or not check_password(input.password, user.password):
            raise UnauthorizedException("Invalid credentials")

        tokens = await self.tokenService.assign_auth_tokens(user)

        return TAuthTokens(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )
