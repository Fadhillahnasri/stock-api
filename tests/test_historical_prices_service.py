from app.services import stock_service


def test_get_historical_prices(monkeypatch):
    expected = {
        "symbol": "BBCA.JK",
        "period": "1y",
        "interval": "1d",
        "data": [
            {
                "date": "2026-01-02",
                "open": 8000,
                "high": 8100,
                "low": 7950,
                "close": 8050,
                "volume": 1000000,
            }
        ],
    }

    def mock_get_historical_prices(
        symbol,
        period="1y",
        interval="1d"
    ):
        assert symbol == "BBCA.JK"
        assert period == "1y"
        assert interval == "1d"

        return expected

    monkeypatch.setattr(
        stock_service.provider,
        "get_historical_prices",
        mock_get_historical_prices,
    )

    result = stock_service.get_historical_prices(
        symbol="bbca.jk"
    )

    assert result == expected
    assert result["symbol"] == "BBCA.JK"
    assert len(result["data"]) == 1
    assert result["data"][0]["close"] == 8050