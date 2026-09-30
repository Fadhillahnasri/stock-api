from app.utils.logger import logger

from app.services.portfolio_analysis_service import get_portfolio_analysis
from app.services.historical_analysis_service import (
    calculate_scenario_stock_return,
)
from app.services.historical_scenario_service import (
    get_historical_scenarios,
    get_historical_scenario,
)

def calculate_portfolio_stress_impact(
    portfolio_stocks: list,
    scenario_returns: list
):
    logger.info(
        "Stress Test - Calculate Portfolio Stress Impact"
    )

    if not portfolio_stocks:
        return None

    return_lookup = {
        item["symbol"]: item
        for item in scenario_returns
    }

    total_weight = 0
    portfolio_return = 0

    stocks = []

    for stock in portfolio_stocks:
        stock_code = stock["stockCode"]
        symbol = f"{stock_code}.JK"

        weight = float(stock.get("portfolioWeight", 0))

        scenario_data = return_lookup.get(symbol)

        if scenario_data is None:
            continue

        stock_return = float(
            scenario_data.get("periodReturn", 0)
        )

        contribution = (
            weight / 100
        ) * stock_return

        portfolio_return += contribution
        total_weight += weight

        stocks.append({
            "stockCode": stock_code,
            "symbol": symbol,
            "portfolioWeight": weight,
            "scenarioReturn": stock_return,
            "scenarioReturnPercentage": stock_return * 100,
            "contribution": contribution,
            "contributionPercentage": contribution * 100,
        })

    if total_weight == 0:
        return None

    return {
        "portfolioReturn": portfolio_return,
        "portfolioReturnPercentage": portfolio_return * 100,
        "totalWeight": total_weight,
        "stocks": stocks,
    }

def run_historical_stress_test(
    portfolio_date: str,
    scenario_id: str
):
    logger.info(
        f"Stress Test - Run Historical Scenario: "
        f"portfolio_date={portfolio_date}, "
        f"scenario={scenario_id}"
    )

    scenario = get_historical_scenario(scenario_id)

    if scenario is None:
        return None

    portfolio = get_portfolio_analysis(
        date=portfolio_date
    )

    if not portfolio or not portfolio.get("stocks"):
        return None

    scenario_returns = []

    for stock in portfolio["stocks"]:
        stock_code = stock["stockCode"]
        symbol = f"{stock_code}.JK"

        result = calculate_scenario_stock_return(
            symbol=symbol,
            scenario_id=scenario_id,
        )

        if result is not None:
            scenario_returns.append(result)

    if not scenario_returns:
        return None

    impact = calculate_portfolio_stress_impact(
        portfolio_stocks=portfolio["stocks"],
        scenario_returns=scenario_returns,
    )

    if impact is None:
        return None

    portfolio_value_before = float(portfolio["totalMarketValue"])
    portfolio_return = float(impact["portfolioReturn"])

    estimated_impact = portfolio_value_before * portfolio_return
    portfolio_value_after = portfolio_value_before + estimated_impact

    impact["portfolioValueBefore"] = portfolio_value_before
    impact["estimatedImpact"] = estimated_impact
    impact["portfolioValueAfter"] = portfolio_value_after

    return {
        "scenario": {
            "id": scenario["id"],
            "name": scenario["name"],
            "startDate": scenario["startDate"],
            "endDate": scenario["endDate"],
            "description": scenario["description"],
            "source": scenario["source"],
        },
        "portfolio": {
            "date": portfolio_date,
            "marketValue": portfolio["totalMarketValue"],
            "costBasis": portfolio["totalCostBasis"],
        },
        "stressTest": impact,
    }