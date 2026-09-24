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