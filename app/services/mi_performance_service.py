from app.services.mi_historical_service import (
    get_mi_historical_snapshot
)
from app.utils.logger import logger


def get_mi_performance(
    start_date: str,
    end_date: str,
    dealer_code: str,
):
    logger.info(
        f"MI Performance - "
        f"{start_date} to {end_date}, "
        f"dealerCode={dealer_code}"
    )

    start_snapshot = get_mi_historical_snapshot(
        date=start_date,
        dealer_code=dealer_code,
    )

    end_snapshot = get_mi_historical_snapshot(
        date=end_date,
        dealer_code=dealer_code,
    )

    start_market_value = start_snapshot["totalMarketValue"]
    end_market_value = end_snapshot["totalMarketValue"]

    start_cost_basis = start_snapshot["totalCostBasis"]
    end_cost_basis = end_snapshot["totalCostBasis"]

    market_value_change = (
        end_market_value - start_market_value
    )

    if start_market_value:
        market_value_change_percentage = (
            market_value_change / start_market_value
        ) * 100
    else:
        market_value_change_percentage = 0

    cost_basis_change = (
        end_cost_basis - start_cost_basis
    )

    return {
        "dealerCode": dealer_code,
        "dealerName": end_snapshot["dealerName"],

        "startDate": start_date,
        "endDate": end_date,

        "startMarketValue": start_market_value,
        "endMarketValue": end_market_value,

        "marketValueChange": market_value_change,
        "marketValueChangePercentage": (
            market_value_change_percentage
        ),

        "startCostBasis": start_cost_basis,
        "endCostBasis": end_cost_basis,
        "costBasisChange": cost_basis_change,

        "startStockCount": start_snapshot["stockCount"],
        "endStockCount": end_snapshot["stockCount"],
    }