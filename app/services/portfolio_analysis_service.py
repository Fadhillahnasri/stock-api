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

        data = response.get("data") or []
        all_data.extend(data)

        total_page = response.get("totalPage") or 1

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

    total_cost_basis = 0.0
    total_market_value = 0.0
    total_unrealized_gain_loss = 0.0
    stocks = []
    skipped_stocks = 0

    for item in all_data:
        stock_code = item.get("stockCode")

        if not stock_code:
            skipped_stocks += 1
            continue

        try:
            net_amount = float(item.get("netAmount") or 0)
            market_value = float(item.get("marketValue") or 0)
            unrealized_gain_loss = float(
                item.get("unrealizedgainorloss") or 0
            )
        except (TypeError, ValueError):
            logger.warning(
                "Portfolio Analysis - Invalid numeric data for %s",
                stock_code,
            )
            skipped_stocks += 1
            continue

        closing_price_raw = item.get("closingPrice")
        try:
            closing_price = (
                float(closing_price_raw)
                if closing_price_raw is not None
                else None
            )
        except (TypeError, ValueError):
            closing_price = None

        total_cost_basis += net_amount
        total_market_value += market_value
        total_unrealized_gain_loss += unrealized_gain_loss

        if net_amount:
            performance_percentage = (
                unrealized_gain_loss / net_amount
            ) * 100
        else:
            performance_percentage = 0.0

        stocks.append({
            "stockCode": stock_code,
            "costBasis": net_amount,
            "marketValue": market_value,
            "unrealizedGainLoss": unrealized_gain_loss,
            "performancePercentage": performance_percentage,
            "portfolioWeight": 0.0,
            "closingPrice": closing_price,
        })

    if not stocks:
        raise ValueError(
            f"Tidak ada data saham valid untuk tanggal {date}"
        )

    if skipped_stocks:
        logger.warning(
            "Portfolio Analysis - Skipped %s invalid stock records",
            skipped_stocks,
        )

    if total_cost_basis:
        unrealized_gain_loss_percentage = (
            total_unrealized_gain_loss / total_cost_basis
        ) * 100
    else:
        unrealized_gain_loss_percentage = 0.0

    for stock in stocks:
        if total_market_value:
            stock["portfolioWeight"] = (
                stock["marketValue"] / total_market_value
            ) * 100

    stocks_sorted = sorted(
        stocks,
        key=lambda x: x["performancePercentage"],
        reverse=True,
    )

    top_gainers = stocks_sorted[:5]
    top_losers = list(reversed(stocks_sorted[-5:]))

    return {
        "totalCostBasis": total_cost_basis,
        "totalMarketValue": total_market_value,
        "totalUnrealizedGainLoss": total_unrealized_gain_loss,
        "totalUnrealizedGainLossPercentage": (
            unrealized_gain_loss_percentage
        ),
        "stocks": stocks,
        "topGainers": top_gainers,
        "topLosers": top_losers,
    }
