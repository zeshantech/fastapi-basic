from fastapi import Request, Depends
from app.common.types import TCurrentUser
from app.common.exceptions import InternalServerErrorException
from app.auth.auth_middleware import get_current_user_from_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def current_user(
    request: Request = None,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TCurrentUser:
    try:
        if request and hasattr(request.state, 'user'):
            user = request.state.user
        else:
            # This will be called when using the Depends(current_user) directly
            user = await get_current_user_from_token(credentials)
            
        if not user:
            raise InternalServerErrorException(
                "User not found in request - Please try again in a few seconds"
            )

        return TCurrentUser(
            ID=user.id,
            email=user.email,
        )

    except Exception as e:
        raise InternalServerErrorException(
            f"Something went wrong while fetching user - {str(e)}"
        )
