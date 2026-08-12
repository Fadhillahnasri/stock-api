import httpx

from app.config import settings


class HttpClient:

    def __init__(self):

        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT
        )

    def get(self, url: str, **kwargs):

        response = self.client.get(
            url,
            **kwargs
        )

        response.raise_for_status()

        return response

    def post(self, url: str, **kwargs):

        response = self.client.post(
            url,
            **kwargs
        )

        response.raise_for_status()

        return response

    def close(self):

        self.client.close()