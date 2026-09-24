from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_historical_stock_prices(monkeypatch):
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
        "app.api.routes.get_historical_prices",
        mock_get_historical_prices,
    )

    response = client.get(
        "/stocks/BBCA.JK/history"
    )

    assert response.status_code == 200
    assert response.json() == expected

def test_historical_stock_returns(monkeypatch):
    expected = {
        "symbol": "BBCA.JK",
        "period": "1y",
        "interval": "1d",
        "data": [
            {
                "date": "2026-01-02",
                "close": 8050,
                "dailyReturn": None,
            },
            {
                "date": "2026-01-03",
                "close": 8100,
                "dailyReturn": (8100 / 8050) - 1,
            },
        ],
    }

    monkeypatch.setattr(
        "app.api.routes.calculate_historical_returns",
        lambda symbol, period="1y", interval="1d": expected,
    )

    response = client.get(
        "/stocks/BBCA.JK/history/returns"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["symbol"] == "BBCA.JK"
    assert result["period"] == "1y"
    assert result["interval"] == "1d"

    assert len(result["data"]) == 2

    assert result["data"][0]["dailyReturn"] is None

    assert round(
        result["data"][1]["dailyReturn"],
        6
    ) == round(
        (8100 / 8050) - 1,
        6
    )

def test_historical_stock_sensitivity(monkeypatch):
    expected = {
        "beta": 1.25,
        "observationCount": 100,
        "dates": [
            "2026-01-01",
            "2026-01-02",
        ],
        "stockReturns": [
            0.02,
            -0.01,
        ],
        "benchmarkReturns": [
            0.015,
            -0.005,
        ],
    }

    monkeypatch.setattr(
        "app.api.routes.get_stock_sensitivity",
        lambda symbol, benchmark_symbol="^JKSE", period="1y", interval="1d": expected,
    )

    response = client.get(
        "/stocks/BBCA.JK/sensitivity"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["beta"] == 1.25
    assert result["observationCount"] == 100

    assert result["dates"] == [
        "2026-01-01",
        "2026-01-02",
    ]

    assert result["stockReturns"] == [
        0.02,
        -0.01,
    ]

    assert result["benchmarkReturns"] == [
        0.015,
        -0.005,
    ]