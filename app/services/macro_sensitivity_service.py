from app.utils.logger import logger


def calculate_macro_sensitivity(
    stock_data: list,
    macro_data: list
):
    logger.info(
        "Macro Sensitivity - Calculate Stock vs Macro"
    )

    if not stock_data or not macro_data:
        return None

    # =========================
    # 1. Prepare stock returns
    # =========================
    stock_lookup = {
        item["date"]: float(item["dailyReturn"])
        for item in stock_data
        if item.get("dailyReturn") is not None
    }

    # =========================
    # 2. Calculate macro returns
    # =========================
    sorted_macro_data = sorted(
        [
            item for item in macro_data
            if item.get("value") is not None
        ],
        key=lambda item: item["date"]
    )

    macro_returns = {}

    previous_value = None

    for item in sorted_macro_data:
        date = item["date"]
        value = float(item["value"])

        if previous_value is None:
            previous_value = value
            continue

        if previous_value == 0:
            previous_value = value
            continue

        macro_return = (value / previous_value) - 1

        macro_returns[date] = macro_return

        previous_value = value

    # =========================
    # 3. Match stock & macro
    # =========================
    common_dates = sorted(
        set(stock_lookup.keys())
        & set(macro_returns.keys())
    )

    if len(common_dates) < 2:
        return None

    stock_returns = [
        stock_lookup[date]
        for date in common_dates
    ]

    macro_return_values = [
        macro_returns[date]
        for date in common_dates
    ]

    # =========================
    # 4. Calculate means
    # =========================
    mean_stock = (
        sum(stock_returns)
        / len(stock_returns)
    )

    mean_macro = (
        sum(macro_return_values)
        / len(macro_return_values)
    )

    # =========================
    # 5. Calculate covariance
    # =========================
    covariance = sum(
        (stock_return - mean_stock)
        * (macro_return - mean_macro)
        for stock_return, macro_return
        in zip(
            stock_returns,
            macro_return_values
        )
    ) / len(stock_returns)

    # =========================
    # 6. Calculate macro variance
    # =========================
    macro_variance = sum(
        (macro_return - mean_macro) ** 2
        for macro_return in macro_return_values
    ) / len(macro_return_values)

    if macro_variance == 0:
        return None

    # =========================
    # 7. Calculate Beta
    # =========================
    beta = covariance / macro_variance

    # =========================
    # 8. Calculate stock variance
    # =========================
    stock_variance = sum(
        (stock_return - mean_stock) ** 2
        for stock_return in stock_returns
    ) / len(stock_returns)

    # =========================
    # 9. Calculate Correlation
    # =========================
    if stock_variance == 0:
        correlation = 0
    else:
        correlation = (
            covariance
            / (
                stock_variance ** 0.5
                * macro_variance ** 0.5
            )
        )

    # =========================
    # 10. Return result
    # =========================
    return {
        "beta": beta,
        "correlation": correlation,
        "observations": len(common_dates),
        "startDate": common_dates[0],
        "endDate": common_dates[-1],
    }