import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.exceptions.provider_exceptions import ProviderTimeoutError
from app.exceptions.provider_exceptions import ProviderConnectionError
from app.providers.internal_provider import InternalProvider
from app.exceptions.provider_exceptions import ProviderError

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["message"] == "API is running"


def test_stock_valid():
    response = client.get("/stock/BBCA.JK")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["provider"] == "Yahoo Finance"
    assert data["data"]["symbol"] == "BBCA.JK"
    assert data["data"]["company_name"]
    assert data["data"]["current_price"] is not None

def test_stock_invalid():
    response = client.get("/stock/ABC123.JK")

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["status"] == 404
    assert "not found" in data["message"].lower()

def test_multiple_stocks():
    response = client.get(
        "/stocks?symbols=BBCA.JK,BBRI.JK,BMRI.JK"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["provider"] == "Yahoo Finance"
    assert data["total"] == 3
    assert len(data["data"]) == 3
    assert data["failed"] == []

def test_multiple_stocks_with_invalid():
    response = client.get(
        "/stocks?symbols=BBCA.JK,ABC123.JK,BBRI.JK"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["total"] == 2
    assert len(data["data"]) == 2
    assert "ABC123.JK" in data["failed"]

def test_company_valid():
    response = client.get("/company/BBCA.JK")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["provider"] == "Yahoo Finance"
    assert data["data"]["symbol"] == "BBCA.JK"
    assert data["data"]["company_name"]
    assert data["data"]["exchange"]
    assert data["data"]["country"]


def test_company_invalid():
    response = client.get("/company/ABC123.JK")

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["status"] == 404
    assert "not found" in data["message"].lower()

def test_provider_error(monkeypatch):
    from app.services import stock_service
    from app.exceptions.provider_exceptions import ProviderError

    class ErrorProvider:
        def get_stock_price(self, symbol):
            raise ProviderError("Test provider error")

    monkeypatch.setattr(stock_service, "provider", ErrorProvider())

    response = client.get("/stock/BBCA.JK")

    assert response.status_code == 502

    data = response.json()

    assert data["success"] is False
    assert data["status"] == 502
    assert data["message"] == "Test provider error"

def test_provider_timeout(monkeypatch):
    from app.services import stock_service

    class TimeoutProvider:
        def get_stock_price(self, symbol):
            raise ProviderTimeoutError(
                "Yahoo Finance request timed out"
            )

    monkeypatch.setattr(
        stock_service,
        "provider",
        TimeoutProvider()
    )

    response = client.get("/stock/BBCA.JK")

    assert response.status_code == 502

    data = response.json()

    assert data["success"] is False
    assert data["status"] == 502
    assert data["message"] == "Yahoo Finance request timed out"
    assert data["path"] == "/stock/BBCA.JK"


def test_provider_connection_error(monkeypatch):
    from app.services import stock_service

    class ConnectionErrorProvider:
        def get_stock_price(self, symbol):
            raise ProviderConnectionError(
                "Unable to connect to Yahoo Finance"
            )

    monkeypatch.setattr(
        stock_service,
        "provider",
        ConnectionErrorProvider()
    )

    response = client.get("/stock/BBCA.JK")

    assert response.status_code == 502

    data = response.json()

    assert data["success"] is False
    assert data["status"] == 502
    assert data["message"] == "Unable to connect to Yahoo Finance"
    assert data["path"] == "/stock/BBCA.JK"


def test_internal_provider_not_implemented():
    provider = InternalProvider()

    with pytest.raises(ProviderError) as exc:
        provider.get_stock_price("BBCA.JK")

    assert str(exc.value) == "Internal Provider belum diimplementasikan."

    provider.client.close()