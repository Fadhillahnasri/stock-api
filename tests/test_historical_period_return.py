
from app.services.historical_analysis_service import (
    calculate_period_return,
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