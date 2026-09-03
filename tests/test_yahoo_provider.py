import pytest

from app.providers.yahoo_provider import YahooProvider
from app.exceptions.provider_exceptions import ProviderError


def test_get_stock_price_success(monkeypatch):
    class MockTicker:
        @property
        def info(self):
            return {
                "currentPrice": 9000,
                "longName": "PT Bank Central Asia Tbk",
                "dayHigh": 9100,
                "dayLow": 8900,
                "open": 8950,
                "previousClose": 8950,
                "regularMarketChange": 50,
                "regularMarketChangePercent": 0.56,
                "currency": "IDR",
                "exchange": "JKT",
                "marketState": "REGULAR"
            }

    monkeypatch.setattr(
        "app.providers.yahoo_provider.yf.Ticker",
        lambda symbol: MockTicker()
    )

    provider = YahooProvider()

    result = provider.get_stock_price("bbca.jk")

    assert result["symbol"] == "BBCA.JK"
    assert result["company_name"] == "PT Bank Central Asia Tbk"
    assert result["current_price"] == 9000
    assert result["currency"] == "IDR"


def test_get_stock_price_invalid(monkeypatch):
    class MockTicker:
        @property
        def info(self):
            return {}

    monkeypatch.setattr(
        "app.providers.yahoo_provider.yf.Ticker",
        lambda symbol: MockTicker()
    )

    provider = YahooProvider()

    result = provider.get_stock_price("ABC123.JK")

    assert result is None


def test_get_stock_price_provider_error(monkeypatch):
    def mock_ticker(symbol):
        raise Exception("Yahoo Finance failed")

    monkeypatch.setattr(
        "app.providers.yahoo_provider.yf.Ticker",
        mock_ticker
    )

    provider = YahooProvider()

    with pytest.raises(ProviderError) as exc:
        provider.get_stock_price("BBCA.JK")

    assert str(exc.value) == "Yahoo Finance error for BBCA.JK"


def test_get_company_profile_success(monkeypatch):
    class MockTicker:
        @property
        def info(self):
            return {
                "longName": "PT Bank Central Asia Tbk",
                "exchange": "JKT",
                "sector": "Financial Services",
                "industry": "Banks - Diversified",
                "country": "Indonesia",
                "website": "https://www.bca.co.id",
                "fullTimeEmployees": 28000,
                "currency": "IDR"
            }

    monkeypatch.setattr(
        "app.providers.yahoo_provider.yf.Ticker",
        lambda symbol: MockTicker()
    )

    provider = YahooProvider()

    result = provider.get_company_profile("bbca.jk")

    assert result["symbol"] == "BBCA.JK"
    assert result["company_name"] == "PT Bank Central Asia Tbk"
    assert result["exchange"] == "JKT"
    assert result["country"] == "Indonesia"
    assert result["currency"] == "IDR"


def test_get_company_profile_invalid(monkeypatch):
    class MockTicker:
        @property
        def info(self):
            return {
                "exchange": "JKT",
                "country": "Indonesia"
            }

    monkeypatch.setattr(
        "app.providers.yahoo_provider.yf.Ticker",
        lambda symbol: MockTicker()
    )

    provider = YahooProvider()

    result = provider.get_company_profile("ABC123.JK")

    assert result is None