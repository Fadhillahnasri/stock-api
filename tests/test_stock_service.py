from app.services import stock_service


def test_get_stock_price(monkeypatch):
    class MockProvider:
        def get_stock_price(self, symbol):
            return {
                "symbol": symbol,
                "company_name": "PT Bank Central Asia Tbk",
                "current_price": 9000
            }

    monkeypatch.setattr(
        stock_service,
        "provider",
        MockProvider()
    )

    result = stock_service.get_stock_price(" bbca.jk ")

    assert result["symbol"] == "BBCA.JK"
    assert result["company_name"] == "PT Bank Central Asia Tbk"
    assert result["current_price"] == 9000


def test_get_company_profile(monkeypatch):
    class MockProvider:
        def get_company_profile(self, symbol):
            return {
                "symbol": symbol,
                "company_name": "PT Bank Central Asia Tbk",
                "country": "Indonesia"
            }

    monkeypatch.setattr(
        stock_service,
        "provider",
        MockProvider()
    )

    result = stock_service.get_company_profile(" bbca.jk ")

    assert result["symbol"] == "BBCA.JK"
    assert result["company_name"] == "PT Bank Central Asia Tbk"
    assert result["country"] == "Indonesia"


def test_get_multiple_stocks(monkeypatch):
    class MockProvider:
        def get_stock_price(self, symbol):
            stocks = {
                "BBCA.JK": {
                    "symbol": "BBCA.JK",
                    "current_price": 9000
                },
                "BBRI.JK": {
                    "symbol": "BBRI.JK",
                    "current_price": 4500
                }
            }

            return stocks.get(symbol)

    monkeypatch.setattr(
        stock_service,
        "provider",
        MockProvider()
    )

    result = stock_service.get_multiple_stocks(
        ["BBCA.JK", "ABC123.JK", "BBRI.JK"]
    )

    assert result["total"] == 2
    assert result["failed"] == ["ABC123.JK"]
    assert len(result["data"]) == 2
    assert result["data"][0]["symbol"] == "BBCA.JK"
    assert result["data"][1]["symbol"] == "BBRI.JK"