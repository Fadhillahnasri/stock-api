import math

from app.services.stock_service import get_historical_prices
from app.services.historical_scenario_service import (
    get_historical_scenario,
)
from app.utils.logger import logger


def calculate_period_return(
    symbol: str,
    start_date: str,
    end_date: str,
    historical_data: dict
):
    """
    Menghitung return saham berdasarkan harga penutupan
    pertama dan terakhir dalam periode skenario.

    Mengabaikan data dengan harga tidak valid dan, jika
    tersedia, data dengan volume nol. Mengembalikan None
    jika data tidak memadai atau harga tidak bergerak
    sama sekali sepanjang periode.
    """

    prices = [
        item
        for item in historical_data.get("data", [])
        if start_date <= item.get("date", "") <= end_date
    ]

    prices.sort(key=lambda item: item.get("date", ""))

    valid_prices = []

    for item in prices:
        try:
            close = float(item["close"])
        except (KeyError, TypeError, ValueError):
            continue

        if not math.isfinite(close) or close <= 0:
            continue

        # Jika volume tersedia, abaikan data dengan volume nol
        if item.get("volume") is not None:
            try:
                volume = float(item["volume"])
            except (TypeError, ValueError):
                continue

            if not math.isfinite(volume) or volume <= 0:
                continue

        valid_prices.append({
            "date": item["date"],
            "close": close,
        })

    if len(valid_prices) < 2:
        return None

    start_data = valid_prices[0]
    end_data = valid_prices[-1]

    start_price = start_data["close"]
    end_price = end_data["close"]

    # Jangan menganggap harga yang konstan sebagai return
    # yang valid untuk skenario stress test.
    if all(
        item["close"] == start_price
        for item in valid_prices
    ):
        return None

    period_return = (end_price / start_price) - 1

    return {
        "symbol": symbol.strip().upper(),
        "startDate": start_data["date"],
        "endDate": end_data["date"],
        "startPrice": start_price,
        "endPrice": end_price,
        "periodReturn": period_return,
        "periodReturnPercentage": period_return * 100,
    }


def calculate_historical_returns(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
):
    symbol = symbol.strip().upper()

    logger.info(
        f"Historical Analysis - Calculate Daily Returns: "
        f"{symbol}, period={period}, interval={interval}"
    )

    historical_data = get_historical_prices(
        symbol=symbol,
        period=period,
        interval=interval
    )

    if not historical_data or not historical_data.get("data"):
        return None

    prices = historical_data["data"]
    prices.sort(key=lambda item: item["date"])

   
    returns = []
    previous_close = None

    for item in prices:
        try:
            close = float(item["close"])
        except (KeyError, TypeError, ValueError):
            previous_close = None
            continue

        if not math.isfinite(close) or close <= 0:
            previous_close = None
            continue

        daily_return = None

        if previous_close is not None:
            daily_return = (close / previous_close) - 1

        returns.append({
            "date": item["date"],
            "close": close,
            "dailyReturn": daily_return,
            "dailyReturnPercentage": (
                daily_return * 100
                if daily_return is not None
                else None
            ),
        })

        previous_close = close


    return {
        "symbol": symbol,
        "period": period,
        "interval": interval,
        "data": returns,
    }


def calculate_scenario_stock_return(
    symbol: str,
    scenario_id: str
):
    symbol = symbol.strip().upper()

    logger.info(
        f"Historical Analysis - Calculate Scenario Return: "
        f"{symbol}, scenario={scenario_id}"
    )

    scenario = get_historical_scenario(scenario_id)

    if scenario is None:
        return None

    historical_data = get_historical_prices(
        symbol=symbol,
        period="max",
        interval="1d"
    )

    if not historical_data or not historical_data.get("data"):
        return None

    result = calculate_period_return(
        symbol=symbol,
        start_date=scenario["startDate"],
        end_date=scenario["endDate"],
        historical_data=historical_data,
    )

    if result is None:
        return None

    return {
        **result,
        "scenarioId": scenario["id"],
        "scenarioName": scenario["name"],
        "scenarioStartDate": scenario["startDate"],
        "scenarioEndDate": scenario["endDate"],
    }