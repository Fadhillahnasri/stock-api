import httpx

from app.config import settings


class HttpClient:

    def __init__(self):

        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT
        )

    def get(self, url: str, **kwargs):

        return self.client.get(
            url,
            **kwargs
        )

    def post(self, url: str, **kwargs):

        return self.client.post(
            url,
            **kwargs
        )

    def close(self):

        self.client.close()