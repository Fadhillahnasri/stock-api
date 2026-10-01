from app.utils.logger import logger


def calculate_oil_price_sensitivity(
    stock_data: list,
    oil_data: list
):
    logger.info(
        "Oil Price Sensitivity - Calculate Stock vs Oil"
    )

    if not stock_data or not oil_data:
        return None

    stock_lookup = {
        item["date"]: float(item["dailyReturn"])
        for item in stock_data
        if item.get("dailyReturn") is not None
    }

    sorted_oil_data = sorted(
        [
            item
            for item in oil_data
            if item.get("value") is not None
        ],
        key=lambda item: item["date"]
    )

    oil_returns = {}
    previous_value = None

    for item in sorted_oil_data:
        date = item["date"]
        value = float(item["value"])

        if previous_value is None:
            previous_value = value
            continue

        if previous_value == 0:
            previous_value = value
            continue

        oil_return = (value / previous_value) - 1

        oil_returns[date] = oil_return

        previous_value = value

    common_dates = sorted(
        set(stock_lookup.keys()) &
        set(oil_returns.keys())
    )

    if len(common_dates) < 2:
        return None

    stock_returns = [
        stock_lookup[date]
        for date in common_dates
    ]

    oil_return_values = [
        oil_returns[date]
        for date in common_dates
    ]

    mean_stock = (
        sum(stock_returns) /
        len(stock_returns)
    )

    mean_oil = (
        sum(oil_return_values) /
        len(oil_return_values)
    )

    covariance = sum(
        (stock_return - mean_stock) *
        (oil_return - mean_oil)
        for stock_return, oil_return
        in zip(stock_returns, oil_return_values)
    ) / len(stock_returns)

    oil_variance = sum(
        (oil_return - mean_oil) ** 2
        for oil_return in oil_return_values
    ) / len(oil_return_values)

    if oil_variance == 0:
        return None

    beta = covariance / oil_variance

    stock_variance = sum(
        (stock_return - mean_stock) ** 2
        for stock_return in stock_returns
    ) / len(stock_returns)

    if stock_variance == 0:
        correlation = 0
    else:
        correlation = (
            covariance /
            (
                stock_variance ** 0.5 *
                oil_variance ** 0.5
            )
        )

    return {
        "beta": beta,
        "correlation": correlation,
        "observations": len(common_dates),
        "startDate": common_dates[0],
        "endDate": common_dates[-1],
    }