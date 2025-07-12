from uuid import UUID
from app.common.exceptions import NotFoundException
from app.user.user_model import User
from app.user.user_schema import UserCreate
from app.common.utils import hash_password

class UserService:
    async def create_user(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            password=hash_password(data.password),
            full_name=data.full_name,
        )

        await user.save()
        return user

    async def find_user_by_email(self, email: str) -> User | None:
        user = await User.get_or_none(email=email)

        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await User.get_or_none(ID=user_id)
        if not user:
            raise NotFoundException("User not found")

        return user
