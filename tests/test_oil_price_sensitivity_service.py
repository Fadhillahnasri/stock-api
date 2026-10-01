from app.services.oil_price_sensitivity_service import (
    calculate_oil_price_sensitivity,
)


def test_calculate_oil_price_sensitivity():
    stock_data = [
        {
            "date": "2026-09-27",
            "dailyReturn": 0.01
        },
        {
            "date": "2026-09-28",
            "dailyReturn": 0.02
        },
        {
            "date": "2026-09-29",
            "dailyReturn": 0.03
        },
    ]

    oil_data = [
        {
            "date": "2026-09-27",
            "value": 90
        },
        {
            "date": "2026-09-28",
            "value": 91
        },
        {
            "date": "2026-09-29",
            "value": 93
        },
    ]

    result = calculate_oil_price_sensitivity(
        stock_data=stock_data,
        oil_data=oil_data
    )

    assert result is not None
    assert "beta" in result
    assert "correlation" in result
    assert "observations" in result

    assert result["observations"] == 2
    assert result["startDate"] == "2026-09-28"
    assert result["endDate"] == "2026-09-29"