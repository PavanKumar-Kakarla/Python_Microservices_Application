from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.gateway_service import GatewayService


router = APIRouter(
    prefix="/gateway/cart",
    tags=["Cart"]
)

security = HTTPBearer()

def get_headers(request: Request):

    authorization = request.headers.get("Authorization")

    headers = {}

    if authorization:
        headers["Authorization"] = authorization

    return headers


@router.get("")
def get_cart(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):

    headers = get_headers(request)

    return GatewayService.get_cart(headers)


@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_item(
    data: dict,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    headers = get_headers(request)

    return GatewayService.add_item(
        data=data,
        headers=headers
    )


@router.put("/items/{product_id}")
def update_item(
    product_id: int,
    data: dict,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    headers = get_headers(request)

    return GatewayService.update_item(
        product_id=product_id,
        data=data,
        headers=headers,
    )


@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    product_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    headers = get_headers(request)

    GatewayService.remove_item(
        headers=headers,
        product_id=product_id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    headers = get_headers(request)

    GatewayService.clear_cart(
        headers=headers
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)