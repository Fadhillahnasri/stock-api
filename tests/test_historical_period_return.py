
from app.services.historical_analysis_service import (
    calculate_period_return,
    calculate_scenario_stock_return,
)


def test_calculate_period_return():
    historical_data = {
        "symbol": "BBCA.JK",
        "data": [
            {"date": "2020-03-02", "close": 6000},
            {"date": "2020-03-03", "close": 5700},
            {"date": "2020-03-04", "close": 5400},
        ],
    }

    result = calculate_period_return(
        symbol="BBCA.JK",
        start_date="2020-03-02",
        end_date="2020-03-04",
        historical_data=historical_data,
    )

    assert result["symbol"] == "BBCA.JK"
    assert result["startPrice"] == 6000
    assert result["endPrice"] == 5400
    assert round(result["periodReturn"], 2) == -0.10
    assert round(result["periodReturnPercentage"], 2) == -10.0


def test_calculate_period_return_insufficient_data():
    historical_data = {
        "symbol": "BBCA.JK",
        "data": [
            {"date": "2020-03-02", "close": 6000},
        ],
    }

    result = calculate_period_return(
        symbol="BBCA.JK",
        start_date="2020-03-02",
        end_date="2020-03-04",
        historical_data=historical_data,
    )

    assert result is None

def test_calculate_scenario_stock_return(monkeypatch):
    historical_data = {
        "symbol": "BBCA.JK",
        "period": "max",
        "interval": "1d",
        "data": [
            {
                "date": "2020-02-19",
                "close": 6000,
            },
            {
                "date": "2020-03-23",
                "close": 4500,
            },
        ],
    }

    monkeypatch.setattr(
        "app.services.historical_analysis_service.get_historical_prices",
        lambda symbol, period, interval: historical_data,
    )

    result = calculate_scenario_stock_return(
        symbol="BBCA.JK",
        scenario_id="covid_2020",
    )


    assert result is not None
    assert result["symbol"] == "BBCA.JK"
    assert result["scenarioId"] == "covid_2020"
    assert result["startPrice"] == 6000
    assert result["endPrice"] == 4500
    assert round(result["periodReturn"], 2) == -0.25
    assert round(result["periodReturnPercentage"], 2) == -25.0