from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.gateway_service import GatewayService


router = APIRouter(
    prefix="/gateway/products",
    tags=["Products"]
)

security = HTTPBearer()

def get_headers(request: Request):

    authorization = request.headers.get("Authorization")

    headers = {}

    if authorization:
        headers["Authorization"] = authorization

    return headers


@router.get("")
def get_products(request: Request):

    headers = get_headers(request)

    return GatewayService.get_products(headers)


@router.get("/{product_id}")
def get_product(product_id: int, request: Request):

    headers = get_headers(request)

    return GatewayService.get_product(
        product_id=product_id,
        headers=headers
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    data: dict,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    headers = get_headers(request)

    return GatewayService.create_product(
        data=data,
        headers=headers
    )


@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: dict,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    headers = get_headers(request)

    return GatewayService.update_product(
        product_id=product_id,
        data=data,
        headers=headers
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    headers = get_headers(request)

    GatewayService.delete_product(
        product_id=product_id,
        headers=headers
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)