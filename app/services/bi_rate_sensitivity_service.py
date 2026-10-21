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

    # Simpan harga penutupan saham yang valid.
    stock_prices = {
        item["date"]: float(item["close"])
        for item in stock_data
        if item.get("date")
        and item.get("close") is not None
        and float(item["close"]) > 0
    }

    if not stock_prices:
        return None

    # Urutkan tanggal perdagangan saham.
    stock_dates = sorted(stock_prices.keys())

    # Urutkan data BI-Rate berdasarkan tanggal.
    sorted_bi_rate = sorted(
        bi_rate_data,
        key=lambda item: item["date"]
    )

    events = []
    previous_rate = None

    for item in sorted_bi_rate:
        event_date = item["date"]
        current_rate = float(item["value"])

        if previous_rate is None:
            previous_rate = current_rate
            continue

        change_bps = round(
            (current_rate - previous_rate) * 100,
            6
        )

        # Hanya proses event ketika BI-Rate berubah.
        if change_bps == 0:
            previous_rate = current_rate
            continue

        previous_stock_date = None
        current_stock_date = None

        # Cari tanggal perdagangan sebelum tanggal event.
        for stock_date in stock_dates:
            if stock_date < event_date:
                previous_stock_date = stock_date
            else:
                # Tanggal event atau hari perdagangan
                # pertama setelah tanggal event.
                current_stock_date = stock_date
                break

        event_return = None

        if previous_stock_date and current_stock_date:
            previous_stock_price = stock_prices[
                previous_stock_date
            ]
            current_stock_price = stock_prices[
                current_stock_date
            ]

            event_return = (
                current_stock_price / previous_stock_price
            ) - 1

        events.append({
            "date": event_date,
            "previousRate": previous_rate,
            "currentRate": current_rate,
            "changeBps": change_bps,
            "stockReturn": event_return,
            "stockReturnPercentage": (
                event_return * 100
                if event_return is not None
                else None
            ),
            "stockReturnDate": current_stock_date,
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