from app.services.stock_service import get_historical_prices
from app.utils.logger import logger

def calculate_beta(
    stock_returns: list[float],
    benchmark_returns: list[float],
):
    logger.info("Sensitivity Analysis - Calculate Beta")

    if len(stock_returns) != len(benchmark_returns):
        raise ValueError(
            "Stock returns and benchmark returns must have the same length."
        )

    if len(stock_returns) < 2:
        return None

    stock_mean = sum(stock_returns) / len(stock_returns)
    benchmark_mean = sum(benchmark_returns) / len(benchmark_returns)

    covariance = sum(
        (stock_return - stock_mean)
        * (benchmark_return - benchmark_mean)
        for stock_return, benchmark_return
        in zip(stock_returns, benchmark_returns)
    ) / (len(stock_returns) - 1)

    benchmark_variance = sum(
        (benchmark_return - benchmark_mean) ** 2
        for benchmark_return in benchmark_returns
    ) / (len(benchmark_returns) - 1)

    if benchmark_variance == 0:
        return None

    return covariance / benchmark_variance

def calculate_stock_sensitivity(
    stock_returns: list[float],
    benchmark_returns: list[float],
):
    logger.info("Sensitivity Analysis - Calculate Stock Sensitivity")

    beta = calculate_beta(
        stock_returns=stock_returns,
        benchmark_returns=benchmark_returns,
    )

    if beta is None:
        return None

    return {
        "beta": beta,
        "observationCount": len(stock_returns),
    }

def align_returns(
    stock_data: list[dict],
    benchmark_data: list[dict],
):
    logger.info("Sensitivity Analysis - Align Historical Returns")

    stock_map = {
        item["date"]: item["dailyReturn"]
        for item in stock_data
        if item.get("dailyReturn") is not None
    }

    benchmark_map = {
        item["date"]: item["dailyReturn"]
        for item in benchmark_data
        if item.get("dailyReturn") is not None
    }

    common_dates = sorted(
        set(stock_map.keys()) & set(benchmark_map.keys())
    )

    stock_returns = []
    benchmark_returns = []
    dates = []

    for date in common_dates:
        dates.append(date)
        stock_returns.append(stock_map[date])
        benchmark_returns.append(benchmark_map[date])

    return {
        "dates": dates,
        "stockReturns": stock_returns,
        "benchmarkReturns": benchmark_returns,
    }

def calculate_sensitivity_analysis(
    stock_data: list[dict],
    benchmark_data: list[dict],
):
    logger.info("Sensitivity Analysis - Calculate Analysis")

    aligned_data = align_returns(
        stock_data=stock_data,
        benchmark_data=benchmark_data,
    )

    if len(aligned_data["dates"]) < 2:
        return None

    sensitivity = calculate_stock_sensitivity(
        stock_returns=aligned_data["stockReturns"],
        benchmark_returns=aligned_data["benchmarkReturns"],
    )

    if sensitivity is None:
        return None

    return {
        "beta": sensitivity["beta"],
        "observationCount": sensitivity["observationCount"],
        "dates": aligned_data["dates"],
        "stockReturns": aligned_data["stockReturns"],
        "benchmarkReturns": aligned_data["benchmarkReturns"],
    }

def get_stock_sensitivity(
    symbol: str,
    benchmark_symbol: str = "^JKSE",
    period: str = "1y",
    interval: str = "1d",
):
    symbol = symbol.strip().upper()
    benchmark_symbol = benchmark_symbol.strip().upper()

    logger.info(
        f"Sensitivity Analysis - Get Stock Sensitivity: "
        f"{symbol} vs {benchmark_symbol}"
    )

    stock_history = get_historical_prices(
        symbol=symbol,
        period=period,
        interval=interval,
    )

    benchmark_history = get_historical_prices(
        symbol=benchmark_symbol,
        period=period,
        interval=interval,
    )

    if not stock_history or not benchmark_history:
        return None

    stock_returns = []

    previous_close = None

    for item in stock_history.get("data", []):
        close = float(item["close"])

        daily_return = (
            None
            if previous_close is None
            else (close / previous_close) - 1
        )

        stock_returns.append({
            "date": item["date"],
            "dailyReturn": daily_return,
        })

        previous_close = close

    benchmark_returns = []

    previous_close = None

    for item in benchmark_history.get("data", []):
        close = float(item["close"])

        daily_return = (
            None
            if previous_close is None
            else (close / previous_close) - 1
        )

        benchmark_returns.append({
            "date": item["date"],
            "dailyReturn": daily_return,
        })

        previous_close = close

    return calculate_sensitivity_analysis(
        stock_data=stock_returns,
        benchmark_data=benchmark_returns,
    )