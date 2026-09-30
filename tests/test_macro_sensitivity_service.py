from app.services.macro_sensitivity_service import (
    calculate_macro_sensitivity
)


def test_calculate_macro_sensitivity():

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

    macro_data = [
        {
            "date": "2026-09-27",
            "value": 17000
        },
        {
            "date": "2026-09-28",
            "value": 17100
        },
        {
            "date": "2026-09-29",
            "value": 17300
        },
    ]

    result = calculate_macro_sensitivity(
        stock_data=stock_data,
        macro_data=macro_data
    )

    assert result is not None

    assert "beta" in result
    assert "correlation" in result
    assert "observations" in result

    assert result["observations"] == 2

    assert result["startDate"] == "2026-09-28"
    assert result["endDate"] == "2026-09-29"


def test_calculate_macro_sensitivity_insufficient_data():

    stock_data = [
        {
            "date": "2026-09-28",
            "dailyReturn": 0.02
        }
    ]

    macro_data = [
        {
            "date": "2026-09-28",
            "value": 17100
        }
    ]

    result = calculate_macro_sensitivity(
        stock_data=stock_data,
        macro_data=macro_data
    )

    assert result is None