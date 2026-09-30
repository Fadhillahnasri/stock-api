from app.providers.macro_provider import MacroProvider
from app.utils.logger import logger


macro_provider = MacroProvider()


def get_exchange_rate(
    currency: str,
    start_date: str,
    end_date: str
):
    currency = currency.strip().upper()

    logger.info(
        f"Macro Service - Get Exchange Rate: "
        f"{currency}, {start_date} to {end_date}"
    )

    result = macro_provider.get_exchange_rate(
        currency=currency,
        start_date=start_date,
        end_date=end_date
    )

    if not result or not result.get("data"):
        logger.warning(
            f"Macro Service - No Exchange Rate Data: "
            f"{currency}, {start_date} to {end_date}"
        )

        return {
            "indicator": f"{currency}/IDR",
            "source": "Bank Indonesia",
            "currency": currency,
            "data": []
        }

    return {
        "indicator": f"{currency}/IDR",
        "source": "Bank Indonesia",
        "currency": currency,
        "data": result["data"]
    }