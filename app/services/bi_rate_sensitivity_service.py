from app.services.stock_service import get_historical_prices
from app.utils.logger import logger


def calculate_bi_rate_events(
    symbol: str,
    bi_rate_data: list,
    stock_historical_data: dict
):
    logger.info(
        f"BI-Rate Sensitivity - Calculate Events: {symbol}"
    )

    if not bi_rate_data or not stock_historical_data:
        return None

    stock_data = stock_historical_data.get("data", [])

    if not stock_data:
        return None

    stock_prices = {
        item["date"]: float(item["close"])
        for item in stock_data
        if item.get("close") is not None
    }

    sorted_bi_rate = sorted(
        bi_rate_data,
        key=lambda item: item["date"]
    )

    events = []
    previous_rate = None

    for item in sorted_bi_rate:
        date = item["date"]
        current_rate = float(item["value"])

        if previous_rate is None:
            previous_rate = current_rate
            continue

        change_bps = (current_rate - previous_rate) * 100

        # Hanya ambil tanggal ketika BI-Rate benar-benar berubah.
        if change_bps == 0:
            previous_rate = current_rate
            continue

        event_return = None

        if date in stock_prices:
            event_dates = sorted(
                stock_date
                for stock_date in stock_prices
                if stock_date < date
            )

            if event_dates:
                previous_stock_date = event_dates[-1]
                previous_stock_price = stock_prices[previous_stock_date]
                current_stock_price = stock_prices[date]

                if previous_stock_price > 0:
                    event_return = (
                        current_stock_price / previous_stock_price
                    ) - 1

        events.append({
            "date": date,
            "previousRate": previous_rate,
            "currentRate": current_rate,
            "changeBps": change_bps,
            "stockReturn": event_return,
            "stockReturnPercentage": (
                event_return * 100
                if event_return is not None
                else None
            ),
        })

        previous_rate = current_rate

    if not events:
        return None

    return {
        "symbol": symbol.strip().upper(),
        "macro": "BI-Rate",
        "events": events,
        "observations": len(events),
    }


def calculate_bi_rate_sensitivity(
    symbol: str,
    start_date: str,
    end_date: str,
    bi_rate_data: list
):
    logger.info(
        f"BI-Rate Sensitivity - "
        f"{symbol}, {start_date} to {end_date}"
    )

    historical_data = get_historical_prices(
        symbol=symbol,
        period="max",
        interval="1d"
    )

    logger.info(
        f"BI-Rate Sensitivity - Historical data received: "
        f"{len(historical_data.get('data', [])) if historical_data else 0} rows"
        )       

    if not historical_data or not historical_data.get("data"):
        return None

    result = calculate_bi_rate_events(
        symbol=symbol,
        bi_rate_data=bi_rate_data,
        stock_historical_data=historical_data
    )

    logger.info(
        f"BI-Rate Sensitivity - Event result: {result}"
    )

    if result is None:
        return None

    # Filter event berdasarkan periode yang diminta.
    filtered_events = [
        event
        for event in result["events"]
        if start_date <= event["date"] <= end_date
    ]

    if not filtered_events:
        return None

    result["events"] = filtered_events
    result["observations"] = len(filtered_events)
    result["startDate"] = filtered_events[0]["date"]
    result["endDate"] = filtered_events[-1]["date"]

    return result