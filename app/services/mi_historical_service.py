from app.services.portfolio_service import get_mi_report
from app.utils.logger import logger


def get_mi_historical_snapshot(
    date: str,
    dealer_code: str,
):
    logger.info(
        f"MI Historical Snapshot - "
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
            f"MI Historical Snapshot - No data: "
            f"date={date}, dealerCode={dealer_code}"
        )

        raise ValueError(
            f"Tidak ada data Fund Manager {dealer_code} "
            f"untuk tanggal {date}"
        )

    dealer_name = all_data[0].get(
        "dealerName",
        dealer_code
    )

    total_cost_basis = 0
    total_market_value = 0
    total_unrealized_gain_loss = 0

    for item in all_data:
        total_cost_basis += float(
            item.get("netAmount", 0)
        )

        total_market_value += float(
            item.get("marketValue", 0)
        )

        total_unrealized_gain_loss += float(
            item.get("unrealizedgainorloss", 0)
        )

    return {
        "dealerCode": dealer_code,
        "dealerName": dealer_name,
        "date": date,
        "stockCount": len(all_data),
        "totalCostBasis": total_cost_basis,
        "totalMarketValue": total_market_value,
        "totalUnrealizedGainLoss": total_unrealized_gain_loss,
    }