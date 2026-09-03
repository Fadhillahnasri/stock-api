import httpx

from app.config import settings
from app.exceptions.provider_exceptions import ProviderTimeoutError

from app.exceptions.provider_exceptions import (
    ProviderTimeoutError,
    ProviderConnectionError
)

class HttpClient:

    def __init__(self):
        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT
        )

    def get(self, url: str, **kwargs):
        try:
            response = self.client.get(
                url,
                **kwargs
            )

            response.raise_for_status()

            return response

        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(
                "Internal API request timed out"
            ) from e

        except httpx.ConnectError as e:
            raise ProviderConnectionError(
                "Unable to connect to Internal API"
            ) from e

    def post(self, url: str, **kwargs):
        try:
            response = self.client.post(
                url,
                **kwargs
            )

            response.raise_for_status()

            return response

        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(
                "Internal API request timed out"
            ) from e

        except httpx.ConnectError as e:
            raise ProviderConnectionError(
                "Unable to connect to Internal API"
            ) from e

    def close(self):
        self.client.close()