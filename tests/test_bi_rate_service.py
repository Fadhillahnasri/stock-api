from unittest.mock import patch

from app.services.macro_service import get_bi_rate


@patch("app.services.macro_service.macro_provider.get_bi_rate")
def test_get_bi_rate(mock_get_bi_rate):
    mock_get_bi_rate.return_value = {
        "indicator": "BI-Rate",
        "source": "Bank Indonesia",
        "data": [
            {
                "date": "2026-05-20",
                "value": 5.25
            },
            {
                "date": "2026-06-09",
                "value": 5.50
            }
        ]
    }

    result = get_bi_rate(
        start_date="2026-05-01",
        end_date="2026-06-30"
    )

    assert result["indicator"] == "BI-Rate"
    assert result["source"] == "Bank Indonesia"
    assert len(result["data"]) == 2


@patch("app.services.macro_service.macro_provider.get_bi_rate")
def test_get_bi_rate_empty_data(mock_get_bi_rate):
    mock_get_bi_rate.return_value = {
        "indicator": "BI-Rate",
        "source": "Bank Indonesia",
        "data": []
    }

    result = get_bi_rate(
        start_date="2027-01-01",
        end_date="2027-01-31"
    )

    assert result["indicator"] == "BI-Rate"
    assert result["source"] == "Bank Indonesia"
    assert result["data"] == []