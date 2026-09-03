import httpx
import pytest

from app.core.http_client import HttpClient
from app.exceptions.provider_exceptions import (
    ProviderTimeoutError,
    ProviderConnectionError
)


def test_http_client_timeout(monkeypatch):
    client = HttpClient()

    def mock_get(*args, **kwargs):
        raise httpx.TimeoutException("timeout")

    monkeypatch.setattr(client.client, "get", mock_get)

    with pytest.raises(ProviderTimeoutError) as exc:
        client.get("http://example.com")

    assert str(exc.value) == "Internal API request timed out"

    client.close()


def test_http_client_connection_error(monkeypatch):
    client = HttpClient()

    def mock_get(*args, **kwargs):
        raise httpx.ConnectError("connection failed")

    monkeypatch.setattr(client.client, "get", mock_get)

    with pytest.raises(ProviderConnectionError) as exc:
        client.get("http://example.com")

    assert str(exc.value) == "Unable to connect to Internal API"

    client.close()

def test_http_client_http_error(monkeypatch):
    client = HttpClient()

    request = httpx.Request(
        "GET",
        "http://example.com"
    )

    response = httpx.Response(
        500,
        request=request
    )

    def mock_get(*args, **kwargs):
        return response

    monkeypatch.setattr(client.client, "get", mock_get)

    with pytest.raises(httpx.HTTPStatusError):
        client.get("http://example.com")

    client.close()