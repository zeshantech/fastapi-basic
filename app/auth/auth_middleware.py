from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.common.types import TCurrentUser
from app.core.token_service import TokenService
from app.user.user_service import UserService
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import UUID

token_service = TokenService()
user_service = UserService()
security = HTTPBearer()


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if self._is_path_protected(request.url.path) and request.method != "OPTIONS":
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)

            token = auth_header.split(" ")[1]
            decoded_token = token_service.verify_auth_token(token)
            if not decoded_token:
                return JSONResponse(
                    {"detail": "Invalid or expired token"}, status_code=401
                )

            user_id = UUID(decoded_token.sub)
            user = await user_service.get_user_by_id(user_id)
            if not user:
                return JSONResponse({"detail": "User not found"}, status_code=401)

            request.state.user = user

        return await call_next(request)

    def _is_path_protected(self, path: str) -> bool:
        """Check if the path should be protected by authentication"""
        public_paths = ["/auth/", "/docs", "/openapi.json", "/redoc", "/"]

        for public_path in public_paths:
            if path.startswith(public_path):
                return False

        return True


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TCurrentUser:
    token = credentials.credentials
    decoded_token = token_service.verify_auth_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = decoded_token.sub
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await user_service.get_user_by_id(UUID(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return TCurrentUser(
        ID=user.ID,
        email=user.email,
    )
