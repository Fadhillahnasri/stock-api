from app.utils.logger import logger

from app.services.portfolio_analysis_service import get_portfolio_analysis
from app.services.historical_analysis_service import (
    calculate_scenario_stock_return,
)
from app.services.historical_scenario_service import (
    get_historical_scenarios,
    get_historical_scenario,
)

from app.services.stress_test_portfolio_service import (
    get_stress_test_portfolios,
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

        period_return = scenario_data.get("periodReturn")

        if period_return is None:
            continue

        stock_return = float(period_return)

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

def run_multi_group_historical_stress_test(
    portfolio_date: str,
    scenario_id: str,
):
    """Menjalankan stress test historis untuk setiap kelompok saham."""

    logger.info(
        f"Multi-group Stress Test: date={portfolio_date}, "
        f"scenario={scenario_id}"
    )

    scenario = get_historical_scenario(scenario_id)

    if scenario is None:
        return None

    portfolio_data = get_stress_test_portfolios(
        date=portfolio_date
    )

    group_results = {}
    return_cache = {}

    for group_name, positions in portfolio_data["groups"].items():
        if not positions:
            group_results[group_name] = {
                "status": "no_data",
                "message": "Tidak ada posisi saham.",
            }
            continue

        # Agregasi nilai pasar untuk kode saham yang sama
        aggregated = {}

        for position in positions:
            code = position["stockCode"]
            aggregated[code] = (
                aggregated.get(code, 0)
                + float(position["marketValue"])
            )

        total_market_value = sum(aggregated.values())

        if total_market_value <= 0:
            group_results[group_name] = {
                "status": "no_data",
                "message": "Total nilai pasar tidak valid.",
            }
            continue

        weighted_stocks = []

        for code, market_value in aggregated.items():
            weighted_stocks.append({
                "stockCode": code,
                "marketValue": market_value,
                "portfolioWeight": (
                    market_value / total_market_value
                ) * 100,
            })

        scenario_returns = []
        missing_stocks = []

        for stock in weighted_stocks:
            code = stock["stockCode"]
            symbol = f"{code}.JK"

            if symbol not in return_cache:
                try:
                    return_cache[symbol] = (
                        calculate_scenario_stock_return(
                            symbol=symbol,
                            scenario_id=scenario_id,
                        )
                    )
                except Exception:
                    logger.exception(
                        f"Gagal menghitung return skenario: {symbol}"
                    )
                    return_cache[symbol] = None

            result = return_cache[symbol]

            if result is None:
                missing_stocks.append(code)
                continue

            scenario_returns.append(result)

        impact = calculate_portfolio_stress_impact(
            portfolio_stocks=weighted_stocks,
            scenario_returns=scenario_returns,
        )

        covered_weight = (
            float(impact["totalWeight"])
            if impact is not None else 0
        )

        if impact is None:
            group_results[group_name] = {
                "status": "insufficient_data",
                "marketValue": total_market_value,
                "coveragePercentage": 0,
                "missingStocks": missing_stocks,
            }
            continue

        
        # Nilai pasar saham yang memiliki hasil return historis
        covered_market_value = sum(
            float(stock["marketValue"])
            for stock in weighted_stocks
            if stock["stockCode"] not in missing_stocks
        )

        # Return portofolio khusus aset yang tercakup.
        # Portfolio weight pada impact masih menggunakan bobot
        # terhadap total nilai pasar grup, sehingga perlu dinormalisasi.
        if covered_market_value <= 0:
            group_results[group_name] = {
                "status": "insufficient_data",
                "marketValue": total_market_value,
                "coveredMarketValue": 0,
                "coveragePercentage": 0,
                "missingStocks": missing_stocks,
            }
            continue

        covered_return = (
            impact["portfolioReturn"]
            * total_market_value
            / covered_market_value
        )

        # Dampak dihitung hanya terhadap aset yang tercakup.
        estimated_impact = (
            covered_market_value * covered_return
        )

        group_results[group_name] = {
            "status": (
                "complete"
                if covered_weight >= 99.99
                else "partial"
            ),
            "marketValue": total_market_value,
            "coveredMarketValue": covered_market_value,
            "portfolioReturn": covered_return,
            "portfolioReturnPercentage": covered_return * 100,
            "estimatedImpact": estimated_impact,
            "portfolioValueAfterCoveredAssets": (
                covered_market_value + estimated_impact
            ),
            "coveragePercentage": covered_weight,
            "missingStocks": missing_stocks,
            "stocks": impact["stocks"],
        }


    return {
        "portfolioDate": portfolio_date,
        "scenario": {
            "id": scenario["id"],
            "name": scenario["name"],
            "startDate": scenario["startDate"],
            "endDate": scenario["endDate"],
            "description": scenario["description"],
            "source": scenario["source"],
        },
        "groups": group_results,
        "includedGroups": portfolio_data["includedGroups"],
        "excludedGroups": portfolio_data["excludedGroups"],
    }