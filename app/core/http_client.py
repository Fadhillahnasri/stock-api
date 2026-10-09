
import threading

import httpx

from app.config import settings
from app.exceptions.provider_exceptions import (
    ProviderTimeoutError,
    ProviderConnectionError,
    ProviderError,
)
from app.utils.logger import logger


class HttpClient:
    def __init__(self):
        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT,
        )

        self.access_token = settings.INTERNAL_API_TOKEN or None
        self.refresh_token = None
        self._auth_lock = threading.RLock()

        self.base_url = settings.INTERNAL_API_BASE_URL.rstrip("/")

    def _login(self):
        """Login untuk memperoleh access token dan refresh token."""
        if not settings.INTERNAL_API_USERNAME or not settings.INTERNAL_API_PASSWORD:
            raise ProviderError(
                "Internal API username/password belum dikonfigurasi."
            )

        try:
            response = self.client.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": settings.INTERNAL_API_USERNAME,
                    "password": settings.INTERNAL_API_PASSWORD,
                },
            )
            response.raise_for_status()
            payload = response.json()

        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(
                "Internal API login timed out"
            ) from e
        except httpx.ConnectError as e:
            raise ProviderConnectionError(
                "Unable to connect to Internal API during login"
            ) from e
        except httpx.HTTPError as e:
            raise ProviderError(
                "Internal API login failed."
            ) from e

        data = payload.get("data", {})
        access_token = data.get("accessToken")
        refresh_token = data.get("refreshToken")

        if payload.get("status") != "success" or not access_token:
            raise ProviderError(
                "Internal API login response tidak valid."
            )

        self.access_token = access_token
        self.refresh_token = refresh_token

   
    def _refresh(self):
        """Memperbarui access token menggunakan refresh token."""
        if not self.refresh_token:
            logger.warning("Token refresh gagal: refresh token tidak tersedia.")
            return False

        try:
            logger.info("Internal API - Mencoba refresh access token.")

            response = self.client.put(
                f"{self.base_url}/auth",
                json={
                    "refreshToken": self.refresh_token,
                },
            )
            response.raise_for_status()
            payload = response.json()

            data = payload.get("data", {})
            access_token = data.get("accessToken")
            refresh_token = data.get("refreshToken")

            if payload.get("status") != "success" or not access_token:
                logger.warning("Internal API - Refresh token gagal: respons tidak valid.")
                return False

            self.access_token = access_token

            if refresh_token:
                self.refresh_token = refresh_token

            logger.info("Internal API - Refresh access token berhasil.")
            return True

        except (httpx.HTTPError, ValueError, TypeError) as e:
            logger.warning(
                "Internal API - Refresh access token gagal: %s",
                type(e).__name__,
            )
            return False


    def _ensure_token(self):
        """Memastikan access token tersedia sebelum request."""
        with self._auth_lock:
            if not self.access_token:
                self._login()

    def _request(self, method: str, url: str, **kwargs):
        try:
            self._ensure_token()

            with self._auth_lock:
                headers = dict(kwargs.pop("headers", {}) or {})
                headers["Authorization"] = (
                    f"Bearer {self.access_token}"
                )

                response = self.client.request(
                    method,
                    url,
                    headers=headers,
                    **kwargs,
                )

                # Refresh hanya jika server mengembalikan HTTP 401.
                if response.status_code == 401:
                    refreshed = self._refresh()

                    if not refreshed:
                        self._login()

                    headers["Authorization"] = (
                        f"Bearer {self.access_token}"
                    )

                    # Ulangi request satu kali saja.
                    response = self.client.request(
                        method,
                        url,
                        headers=headers,
                        **kwargs,
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

    def get(self, url: str, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        return self._request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):
        return self._request("PUT", url, **kwargs)

    def close(self):
        self.client.close()
