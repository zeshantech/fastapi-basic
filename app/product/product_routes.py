from uuid import UUID
from fastapi import APIRouter, Depends, Security
from app.common.schema import MessageOutput
from app.common.types import TCurrentUser
from app.product.product_service import ProductService
from app.product.product_schema import ProductCreate, ProductRead, ProductReadFull
from app.auth.auth_middleware import get_current_user_from_token
from fastapi.security import HTTPBearer

router = APIRouter()
product_service = ProductService()
security = HTTPBearer()


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    current_user: TCurrentUser = Depends(get_current_user_from_token),
):
    return await product_service.create_product(data, current_user)


@router.get("/")
async def get_all_products():
    return await product_service.get_all_products()


@router.get("/{product_id}", response_model=ProductReadFull)
async def get_product_by_id(product_id: UUID):
    return await product_service.get_product_by_id(product_id)


@router.delete("/{product_id}", response_model=MessageOutput)
async def delete_product(
    product_id: UUID, current_user: TCurrentUser = Depends(get_current_user_from_token)
):
    await product_service.delete_product(product_id, current_user)

    return {"message": "Product deleted successfully"}
