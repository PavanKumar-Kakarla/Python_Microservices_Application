import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        elapsed = (time.time() - start) * 1000

        logger.info(
            "%s %s | Status: %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed
        )

        return response