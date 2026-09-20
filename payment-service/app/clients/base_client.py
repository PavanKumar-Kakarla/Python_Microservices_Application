import httpx


class BaseHttpClient:

    @staticmethod
    def get(
        url: str,
        headers: dict | None = None
    ):

        response = httpx.get(
            url,
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response

    @staticmethod
    def post(
        url: str,
        json: dict | None = None,
        headers: dict | None = None
    ):

        response = httpx.post(
            url,
            json=json,
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response

    @staticmethod
    def put(
        url: str,
        json: dict | None = None,
        headers: dict | None = None
    ):

        response = httpx.put(
            url,
            json=json,
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response

    @staticmethod
    def delete(
        url: str,
        headers: dict | None = None
    ):

        response = httpx.delete(
            url,
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response