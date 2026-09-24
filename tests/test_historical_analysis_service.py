from app.services import historical_analysis_service


def test_calculate_historical_returns(monkeypatch):
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
            },
            {
                "date": "2026-01-03",
                "open": 8050,
                "high": 8200,
                "low": 8000,
                "close": 8100,
                "volume": 1200000,
            },
            {
                "date": "2026-01-04",
                "open": 8100,
                "high": 8150,
                "low": 7900,
                "close": 8000,
                "volume": 1100000,
            },
        ],
    }

    monkeypatch.setattr(
        historical_analysis_service,
        "get_historical_prices",
        lambda symbol, period, interval: expected,
    )

    result = historical_analysis_service.calculate_historical_returns(
        symbol="bbca.jk",
        period="1y",
        interval="1d",
    )

    assert result["symbol"] == "BBCA.JK"
    assert len(result["data"]) == 3

    # Data pertama belum memiliki harga sebelumnya
    assert result["data"][0]["dailyReturn"] is None

    # (8100 / 8050) - 1
    assert round(
        result["data"][1]["dailyReturn"],
        6
    ) == round(
        (8100 / 8050) - 1,
        6
    )

    # (8000 / 8100) - 1
    assert round(
        result["data"][2]["dailyReturn"],
        6
    ) == round(
        (8000 / 8100) - 1,
        6
    )