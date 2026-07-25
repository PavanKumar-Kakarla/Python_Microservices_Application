import httpx

from app.core.logger import logger
from app.core.exceptions import GatewayException



class BaseHttpClient:

    TIMEOUT = 5.0


    @classmethod
    def get(cls, url:str, headers: dict | None = None):

        try:

            response = httpx.get(
                url,
                headers=headers,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response


        except httpx.RequestError as ex:

            logger.exception(
                "HTTP Request failed: %s",
                ex
            )

            raise GatewayException(
                status_code=503,
                message="Service unavailable"
            )

        except httpx.HTTPStatusError as ex:

            logger.exception(
                "HTTP Status Error: %s",
                ex
            )

            try:
                message = ex.response.json()
            except Exception:
                message = ex.response.text

            raise GatewayException(
                status_code=ex.response.status_code,
                message=message
            )


    @classmethod
    def post(cls, url: str, headers: dict | None = None, data: dict | None = None):

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

            logger.exception(
                "HTTP Request failed: %s",
                ex
            )

            raise GatewayException(
                status_code=503,
                message="Service unavailable"
            )

        except httpx.HTTPStatusError as ex:

            logger.exception(
                "HTTP Status Error: %s",
                ex
            )

            try:
                message = ex.response.json()
            except Exception:
                message = ex.response.text

            raise GatewayException(
                status_code=ex.response.status_code,
                message=message
            )


    @classmethod
    def put(cls, url: str, headers: dict | None = None, data: dict | None = None):

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

            logger.exception("HTTP Request failed: %s", ex)

            raise GatewayException(
                status_code=503,
                message="Service unavailable"
            )

        except httpx.HTTPStatusError as ex:

            logger.exception("HTTP Status Error: %s", ex)

            try:
                message = ex.response.json()
            except Exception:
                message = ex.response.text

            raise GatewayException(
                status_code=ex.response.status_code,
                message=message
            )


    @classmethod
    def delete(cls, url: str, headers: dict | None = None):

        try:

            response = httpx.delete(
                url,
                headers=headers,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            return response

        
        except httpx.RequestError as ex:

            logger.exception("HTTP Request failed: %s", ex)

            raise GatewayException(
                status_code=503,
                message="Service unavailable"
            )
        
        except httpx.HTTPStatusError as ex:

            logger.exception("HTTP Status Error: %s", ex)

            try:
                message = ex.response.json()
            except Exception:
                message = ex.response.text
        
            raise GatewayException(
                status_code=ex.response.status_code,
                message=message
            )