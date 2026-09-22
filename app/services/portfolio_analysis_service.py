from app.services.portfolio_service import get_index_report
from app.utils.logger import logger


def get_portfolio_analysis():
    logger.info("Portfolio Analysis - Get Portfolio Index Report")

    page = 1
    all_data = []

    while True:
        response = get_index_report(
            params={
                "page": page,
                "limit": 20
            }
        )

        data = response.get("data", [])
        all_data.extend(data)

        total_page = response.get("totalPage", 1)

        if page >= total_page:
            break

        page += 1

    total_cost_basis = 0
    total_market_value = 0
    total_unrealized_gain_loss = 0

    for item in all_data:
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

    stocks = []

    for item in all_data:
        net_amount = float(item.get("netAmount", 0))
        market_value = float(item.get("marketValue", 0))
        unrealized_gain_loss = float(
            item.get("unrealizedgainorloss", 0)
        )

        if total_market_value:
            portfolio_weight = (
                market_value / total_market_value
            ) * 100
        else:
            portfolio_weight = 0

        if net_amount:
            performance_percentage = (
                unrealized_gain_loss / net_amount
            ) * 100
        else:
            performance_percentage = 0

        stocks.append({
            "stockCode": item.get("stockCode"),
            "costBasis": net_amount,
            "marketValue": market_value,
            "unrealizedGainLoss": unrealized_gain_loss,
            "performancePercentage": performance_percentage,
            "portfolioWeight": portfolio_weight,
        })

        stocks_sorted = sorted(
            stocks,
            key=lambda x: x["performancePercentage"],
            reverse=True
        )

        top_gainers = stocks_sorted[:5]
        top_losers = stocks_sorted[-5:]
        top_losers.reverse()

    return {
        "totalCostBasis": total_cost_basis,
        "totalMarketValue": total_market_value,
        "totalUnrealizedGainLoss": total_unrealized_gain_loss,
        "totalUnrealizedGainLossPercentage": unrealized_gain_loss_percentage,
        "stocks": stocks,
        "topGainers": top_gainers,
        "topLosers": top_losers,
    }