from app.services.stock_service import get_historical_prices
from app.utils.logger import logger


def calculate_historical_returns(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
):
    symbol = symbol.strip().upper()

    logger.info(
        f"Historical Analysis - Calculate Returns: "
        f"{symbol}, period={period}, interval={interval}"
    )

    historical_data = get_historical_prices(
        symbol=symbol,
        period=period,
        interval=interval
    )

    if not historical_data or not historical_data.get("data"):
        return None

    data = historical_data["data"]

    results = []

    previous_close = None

    for item in data:
        close = float(item["close"])

        if previous_close is None:
            daily_return = None
        else:
            daily_return = (close / previous_close) - 1

        results.append({
            "date": item["date"],
            "close": close,
            "dailyReturn": daily_return,
        })

        previous_close = close

    return {
        "symbol": historical_data["symbol"],
        "period": historical_data["period"],
        "interval": historical_data["interval"],
        "data": results,
    }


def calculate_period_return(
    symbol: str,
    start_date: str,
    end_date: str,
    historical_data: dict
):
    """
    Menghitung return saham berdasarkan harga penutupan
    pertama dan terakhir dalam periode skenario.

    historical_data berisi data harga yang sudah difilter
    untuk periode start_date hingga end_date.
    """

    prices = [
        item
        for item in historical_data.get("data", [])
        if start_date <= item["date"] <= end_date
    ]

    prices.sort(key=lambda item: item["date"])

    if len(prices) < 2:
        return None

    start_price = float(prices[0]["close"])
    end_price = float(prices[-1]["close"])

    if start_price <= 0:
        return None

    period_return = (end_price / start_price) - 1

    return {
        "symbol": symbol.strip().upper(),
        "startDate": prices[0]["date"],
        "endDate": prices[-1]["date"],
        "startPrice": start_price,
        "endPrice": end_price,
        "periodReturn": period_return,
        "periodReturnPercentage": period_return * 100,
    }