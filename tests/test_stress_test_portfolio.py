from app.services.stress_test_service import (
    calculate_portfolio_stress_impact,
)


def test_calculate_portfolio_stress_impact():

    portfolio_stocks = [
        {
            "stockCode": "BBCA",
            "portfolioWeight": 60,
        },
        {
            "stockCode": "BBRI",
            "portfolioWeight": 40,
        },
    ]

    scenario_returns = [
        {
            "symbol": "BBCA.JK",
            "periodReturn": -0.20,
        },
        {
            "symbol": "BBRI.JK",
            "periodReturn": -0.30,
        },
    ]

    result = calculate_portfolio_stress_impact(
        portfolio_stocks=portfolio_stocks,
        scenario_returns=scenario_returns,
    )

    assert result is not None

    assert result["totalWeight"] == 100

    assert round(
        result["portfolioReturn"],
        2
    ) == -0.24

    assert round(
        result["portfolioReturnPercentage"],
        2
    ) == -24.0

    assert len(result["stocks"]) == 2