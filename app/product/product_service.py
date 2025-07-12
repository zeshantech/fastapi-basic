from app.common.types import TCurrentUser
from app.product.product_model import Product
from app.product.product_schema import ProductCreate, ProductReadFull
from app.ai.ai_service import AIService
from app.product.product_schema import ProductRead
from app.common.exceptions import NotFoundException
from uuid import UUID

from app.user.user_service import UserService


user_service = UserService()


class ProductService:
    def __init__(self):
        self.ai_service = AIService()

    async def create_product(
        self, data: ProductCreate, current_user: TCurrentUser
    ) -> ProductRead:
        user = await user_service.get_user_by_id(current_user.ID)

        embedding = await self.ai_service.embed_text(data.description or data.name)
        product = Product(
            embedding=embedding,
            name=data.name,
            description=data.description,
            price=data.price,
            user=user,
        )

        await product.save()

        return ProductRead.from_orm(product)

    async def get_all_products(self) -> list[ProductRead]:
        products = await Product.all()
        return [ProductRead.from_orm(product) for product in products]

    async def get_product_by_id(self, pid: UUID) -> ProductReadFull:
        product = await Product.get(ID=pid)
        if not product:
            raise NotFoundException("Product not found")

        return ProductReadFull.from_orm(product)

    async def delete_product(self, pid: UUID, current_user: TCurrentUser):
        product = await Product.get(ID=pid, user=current_user.ID)
        if not product:
            raise NotFoundException("Product not found")

        await product.delete()
