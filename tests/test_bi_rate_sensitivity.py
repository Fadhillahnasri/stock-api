
from app.services.bi_rate_sensitivity_service import calculate_bi_rate_events


def test_calculate_bi_rate_event_on_non_trading_day():
    result = calculate_bi_rate_events(
        symbol="BBCA.JK",
        bi_rate_data=[
            {"date": "2025-05-15", "value": 5.75},
            {"date": "2025-05-25", "value": 5.50},
        ],
        stock_historical_data={
            "data": [
                {"date": "2025-05-23", "close": 9000.0},
                {"date": "2025-05-26", "close": 9090.0},
            ]
        },
    )

    assert result is not None
    assert result["observations"] == 1

    event = result["events"][0]

    assert event["date"] == "2025-05-25"
    assert event["changeBps"] == -25
    assert event["stockReturnDate"] == "2025-05-26"
    assert event["stockReturn"] == (9090.0 / 9000.0) - 1
