from app.services.portfolio_service import get_index_report
from app.utils.logger import logger


def get_portfolio_analysis():
    logger.info("Portfolio Analysis - Get Portfolio Index Report")

    response = get_index_report()
    data = response.get("data", [])

    total_cost_basis = 0
    total_market_value = 0
    total_unrealized_gain_loss = 0

    for item in data:
        total_cost_basis += float(item.get("netAmount", 0))
        total_market_value += float(item.get("marketValue", 0))
        total_unrealized_gain_loss += float(
            item.get("unrealizedgainorloss", 0)
        )

    if total_cost_basis:
        unrealized_gain_loss_percentage = (
            total_unrealized_gain_loss / total_cost_basis
        ) * 100
    else:
        unrealized_gain_loss_percentage = 0

    return {
        "totalCostBasis": total_cost_basis,
        "totalMarketValue": total_market_value,
        "totalUnrealizedGainLoss": total_unrealized_gain_loss,
        "totalUnrealizedGainLossPercentage": unrealized_gain_loss_percentage,
    }