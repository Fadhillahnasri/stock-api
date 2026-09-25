from app.services.portfolio_service import get_index_report
from app.utils.logger import logger


def get_portfolio_analysis(date: str):
    logger.info(
        f"Portfolio Analysis - Get Portfolio Index Report: {date}"
    )

    page = 1
    all_data = []

    while True:
        response = get_index_report(
            params={
                "page": page,
                "limit": 20,
                "date": date,
            }
        )

        data = response.get("data", [])
        all_data.extend(data)

        total_page = response.get("totalPage", 1)

        if page >= total_page:
            break

        page += 1

    if not all_data:
        logger.warning(
            f"Portfolio Analysis - No portfolio data for date: {date}"
        )
        raise ValueError(
            f"Tidak ada data portfolio untuk tanggal {date}"
        )

    total_cost_basis = 0
    total_market_value = 0
    total_unrealized_gain_loss = 0

    stocks = []

    for item in all_data:
        stock_code = item.get("stockCode")

        net_amount = float(item.get("netAmount", 0))
        market_value = float(item.get("marketValue", 0))
        unrealized_gain_loss = float(
            item.get("unrealizedgainorloss", 0)
        )
        closing_price = float(item.get("closingPrice", 0))

        total_cost_basis += net_amount
        total_market_value += market_value
        total_unrealized_gain_loss += unrealized_gain_loss

        if net_amount:
            performance_percentage = (
                unrealized_gain_loss / net_amount
            ) * 100
        else:
            performance_percentage = 0

        stocks.append({
            "stockCode": stock_code,
            "costBasis": net_amount,
            "marketValue": market_value,
            "unrealizedGainLoss": unrealized_gain_loss,
            "performancePercentage": performance_percentage,
            "portfolioWeight": 0,
            "closingPrice": closing_price,
        })

    if total_cost_basis:
        unrealized_gain_loss_percentage = (
            total_unrealized_gain_loss / total_cost_basis
        ) * 100
    else:
        unrealized_gain_loss_percentage = 0

    for stock in stocks:
        if total_market_value:
            stock["portfolioWeight"] = (
                stock["marketValue"] / total_market_value
            ) * 100
        else:
            stock["portfolioWeight"] = 0

    stocks_sorted = sorted(
        stocks,
        key=lambda x: x["performancePercentage"],
        reverse=True,
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