
from app.services.historical_scenario_service import (
    get_historical_scenarios,
    get_historical_scenario,
)

from app.services.stress_test_service import (
    calculate_portfolio_stress_impact,
    run_historical_stress_test,
)

def test_get_historical_scenarios():
    result = get_historical_scenarios()

    assert len(result) == 5

    scenario_ids = [
        scenario["id"]
        for scenario in result
    ]

    assert "lehman_2008" in scenario_ids
    assert "greece_2010" in scenario_ids
    assert "oil_2010" in scenario_ids
    assert "trade_war_2018" in scenario_ids
    assert "covid_2020" in scenario_ids


def test_get_historical_scenario():
    result = get_historical_scenario("COVID_2020")

    assert result is not None
    assert result["id"] == "covid_2020"
    assert result["startDate"] == "2020-02-19"
    assert result["endDate"] == "2020-03-23"


def test_get_historical_scenario_not_found():
    result = get_historical_scenario("unknown_scenario")

    assert result is None

def test_run_historical_stress_test(monkeypatch):

    portfolio = {
        "totalMarketValue": 100000000,
        "totalCostBasis": 120000000,
        "stocks": [
            {
                "stockCode": "BBCA",
                "portfolioWeight": 60,
            },
            {
                "stockCode": "BBRI",
                "portfolioWeight": 40,
            },
        ],
    }

    monkeypatch.setattr(
        "app.services.stress_test_service.get_portfolio_analysis",
        lambda date: portfolio,
    )

    def mock_scenario_return(symbol, scenario_id):
        returns = {
            "BBCA.JK": -0.20,
            "BBRI.JK": -0.30,
        }

        return {
            "symbol": symbol,
            "scenarioId": scenario_id,
            "periodReturn": returns[symbol],
        }

    monkeypatch.setattr(
        "app.services.stress_test_service.calculate_scenario_stock_return",
        mock_scenario_return,
    )

    result = run_historical_stress_test(
        portfolio_date="2026-05-26",
        scenario_id="covid_2020",
    )

    assert result is not None

    stress_test = result["stressTest"]

    assert stress_test["portfolioValueBefore"] == 100000000

    expected_impact = (
        100000000
        * stress_test["portfolioReturn"]
    )

    expected_after = (
        100000000
        + expected_impact
    )

    assert stress_test["estimatedImpact"] == expected_impact
    assert stress_test["portfolioValueAfter"] == expected_after

    assert result["scenario"]["id"] == "covid_2020"

    assert result["portfolio"]["date"] == "2026-05-26"

    assert round(
        result["stressTest"]["portfolioReturnPercentage"],
        2,
    ) == -24.0

    assert result["stressTest"]["totalWeight"] == 100

    assert len(result["stressTest"]["stocks"]) == 2