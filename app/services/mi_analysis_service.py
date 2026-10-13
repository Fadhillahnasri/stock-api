from app.services.portfolio_service import get_mi_report
from app.utils.logger import logger


def get_mi_analysis(date: str, dealer_code: str):
    logger.info(
        f"MI Analysis - Get MI Report: "
        f"date={date}, dealerCode={dealer_code}"
    )

    page = 1
    all_data = []

    while True:
        response = get_mi_report(
            params={
                "date": date,
                "page": page,
                "limit": 100,
                "orderBy": "stockCode",
                "dealerCode": dealer_code,
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
            f"MI Analysis - No data for dealerCode: {dealer_code}, "
            f"date: {date}"
        )

        raise ValueError(
            f"Tidak ada data Fund Manager {dealer_code} "
            f"untuk tanggal {date}"
        )

    dealer_name = all_data[0].get("dealerName", dealer_code)

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
        quantity = float(item.get("quantity", 0))
        price = float(item.get("price", 0))

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
            "quantity": quantity,
            "price": price,
            "costBasis": net_amount,
            "marketValue": market_value,
            "unrealizedGainLoss": unrealized_gain_loss,
            "performancePercentage": performance_percentage,
            "portfolioWeight": 0,
            "closingPrice": closing_price,
        })

    if total_cost_basis:
        total_performance_percentage = (
            total_unrealized_gain_loss / total_cost_basis
        ) * 100
    else:
        total_performance_percentage = 0

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
        "dealerCode": dealer_code,
        "dealerName": dealer_name,
        "totalCostBasis": total_cost_basis,
        "totalMarketValue": total_market_value,
        "totalUnrealizedGainLoss": total_unrealized_gain_loss,
        "totalPerformancePercentage": total_performance_percentage,
        "stocks": stocks,
        "topGainers": top_gainers,
        "topLosers": top_losers,
    }