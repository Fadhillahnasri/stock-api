from unittest.mock import patch

from app.services.macro_service import get_exchange_rate


def test_get_exchange_rate():
    mock_data = {
        "currency": "USD",
        "data": [
            {
                "date": "2026-09-29",
                "value": 17965.0,
                "buyRate": 17875.17,
                "sellRate": 18054.83
            }
        ]
    }

    with patch(
        "app.services.macro_service.macro_provider.get_exchange_rate",
        return_value=mock_data
    ):
        result = get_exchange_rate(
            currency="USD",
            start_date="2026-09-29",
            end_date="2026-09-29"
        )

    assert result["indicator"] == "USD/IDR"
    assert result["source"] == "Bank Indonesia"
    assert result["currency"] == "USD"

    assert len(result["data"]) == 1

    assert result["data"][0]["date"] == "2026-09-29"
    assert result["data"][0]["value"] == 17965.0

def test_get_exchange_rate_empty_data():
    mock_data = {
        "currency": "USD",
        "data": []
    }

    with patch(
        "app.services.macro_service.macro_provider.get_exchange_rate",
        return_value=mock_data
    ):
        result = get_exchange_rate(
            currency="USD",
            start_date="2026-09-29",
            end_date="2026-09-29"
        )

    assert result["indicator"] == "USD/IDR"
    assert result["source"] == "Bank Indonesia"
    assert result["currency"] == "USD"
    assert result["data"] == []