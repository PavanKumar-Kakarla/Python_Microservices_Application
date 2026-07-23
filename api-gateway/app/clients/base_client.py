import httpx

from app.core.logger import logger



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

            raise

        except httpx.HTTPStatusError as ex:

            logger.exception(
                "HTTP Status Error: %s",
                ex
            )

            raise
