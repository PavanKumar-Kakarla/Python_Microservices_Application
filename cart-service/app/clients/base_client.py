import httpx


class BaseHttpClient:

    TIMEOUT = 5.0

    @classmethod
    def get(
        cls,
        url: str,
        headers: dict | None = None
    ):
        response = httpx.get(
            url,
            headers=headers,
            timeout=cls.TIMEOUT
        )

        response.raise_for_status()

        return response

    @classmethod
    def post(
        cls,
        url: str,
        json: dict | None = None,
        headers: dict | None = None
    ):
        response = httpx.post(
            url,
            json=json,
            headers=headers,
            timeout=cls.TIMEOUT
        )

        response.raise_for_status()

        return response