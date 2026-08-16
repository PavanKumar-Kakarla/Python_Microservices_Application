import httpx

from fastapi import HTTPException


from app.core.logger import logger
from app.core.exceptions import GatewayException


class BaseHttpClient:

    TIMEOUT = 30.0

    @staticmethod
    def _handle_http_error(ex: httpx.HTTPStatusError):
        logger.warning(
            "Downstream service returned HTTP %s: %s",
            ex.response.status_code,
            ex
        )

        try:
            error_data = ex.response.json()

            if isinstance(error_data, dict):
                message = error_data.get(
                    "detail",
                    error_data.get("message", "Request failed")
                )
            else:
                message = str(error_data)

        except Exception:
            message = ex.response.text or "Request failed"

        raise GatewayException(
            status_code=ex.response.status_code,
            message=message
        )


    @classmethod
    def _handle_request_error(cls, ex):
        if isinstance(ex, httpx.HTTPStatusError):
            logger.warning(
                f"Downstream service returned HTTP "
                f"{ex.response.status_code}: {ex}"
            )

            raise HTTPException(
                status_code=ex.response.status_code,
                detail=ex.response.text
            )

        if isinstance(ex, httpx.ReadTimeout):
            logger.error(
                f"Downstream service request timed out: {ex}"
            )

            raise HTTPException(
                status_code=504,
                detail="Downstream service request timed out"
            )

        if isinstance(ex, httpx.ConnectError):
            logger.error(
                f"Unable to connect to downstream service: {ex}"
            )

            raise HTTPException(
                status_code=503,
                detail="Downstream service is unavailable"
            )

        logger.exception(
            f"Unexpected HTTP client error: {ex}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal gateway error"
        )


    @classmethod
    def get(
        cls,
        url: str,
        headers: dict | None = None
    ):

        try:

            response = httpx.get(
                url,
                headers=headers,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response

        except httpx.RequestError as ex:
            cls._handle_request_error(ex)

        except httpx.HTTPStatusError as ex:
            cls._handle_http_error(ex)

    @classmethod
    def post(
        cls,
        url: str,
        headers: dict | None = None,
        data: dict | None = None
    ):

        try:

            response = httpx.post(
                url,
                headers=headers,
                json=data,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response

        except httpx.RequestError as ex:
            cls._handle_request_error(ex)

        except httpx.HTTPStatusError as ex:
            cls._handle_http_error(ex)

    @classmethod
    def put(
        cls,
        url: str,
        headers: dict | None = None,
        data: dict | None = None
    ):

        try:

            response = httpx.put(
                url,
                headers=headers,
                json=data,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response

        except httpx.RequestError as ex:
            cls._handle_request_error(ex)

        except httpx.HTTPStatusError as ex:
            cls._handle_http_error(ex)

    @classmethod
    def delete(
        cls,
        url: str,
        headers: dict | None = None
    ):

        try:

            response = httpx.delete(
                url,
                headers=headers,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response

        except httpx.RequestError as ex:
            cls._handle_request_error(ex)

        except httpx.HTTPStatusError as ex:
            cls._handle_http_error(ex)