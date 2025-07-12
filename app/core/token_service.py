from datetime import datetime, timedelta, timezone
from redis.asyncio import Redis
from app.core.config import get_settings
import jwt
from app.user.user_model import User
from pydantic import BaseModel
from app.common.exceptions import JwtExpiredException, JwtInvalidException, NotFoundException
import asyncio

class TAuthTokens(BaseModel):
    access_token: str
    refresh_token: str

class TDecodedToken(BaseModel):
    sub: str
    email: str | None = None
    exp: int

class TokenService:
    def __init__(self):
        self.settings = get_settings()
        self.secret_key = self.settings.jwt_secret_key
        self.algorithm = self.settings.jwt_algorithm
        self.access_token_expire = timedelta(
            minutes=self.settings.access_token_expire_minutes
        )
        self.refresh_token_expire = timedelta(
            days=self.settings.refresh_token_expire_days
        )
        self.verification_token_expire = timedelta(
            minutes=self.settings.verification_token_expire_minutes
        )
        self.redis = Redis.from_url(self.settings.redis_uri)

    async def assign_auth_tokens(self, user: User) -> TAuthTokens:
        access_token_expire = datetime.now(timezone.utc) + self.access_token_expire
        refresh_token_expire = datetime.now(timezone.utc) + self.refresh_token_expire

        access_payload = {
            "sub": str(user.ID),
            "email": user.email,
            "exp": access_token_expire,
        }

        refresh_payload = {
            "sub": str(user.ID),
            "exp": refresh_token_expire,
        }

        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        asyncio.create_task(
            self.redis.set(
                f"refresh_token:{user.ID}",
                refresh_token,
                ex=int(self.refresh_token_expire.total_seconds())
            ) # type: ignore
        )

        return TAuthTokens(access_token=access_token, refresh_token=refresh_token)


    def verify_auth_token(self, token: str) -> TDecodedToken:
        decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        if not decoded or "sub" not in decoded or "exp" not in decoded:
            raise JwtInvalidException("Invalid access token")

        return TDecodedToken(sub=str(decoded["sub"]), email=decoded.get("email"), exp=decoded["exp"])

    async def refresh_tokens(self, refresh_token: str) -> TAuthTokens:
        decoded = self.verify_auth_token(refresh_token)

        redis_token = await self.redis.get(f"refresh_token:{decoded.sub}")
        if redis_token is None or redis_token != refresh_token:
            raise JwtExpiredException("Refresh token not found/expired")

        user = await User.get_or_none(ID=decoded.sub)
        if not user:
            raise NotFoundException("User not found")

        tokens = await self.assign_auth_tokens(user)
        return tokens
    

    async def _save_refresh_token(self, user_id: int, token: str) -> None:
        await self.redis.set(
            f"refresh_token:{user_id}",
            token,
            ex=int(self.refresh_token_expire.total_seconds())
        )
