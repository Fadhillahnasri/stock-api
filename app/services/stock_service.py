from app.config import settings
from app.providers.provider_factory import get_provider
from app.utils.logger import logger


provider = get_provider(settings.PROVIDER)


def get_stock_price(symbol: str):

    logger.info(
        f"Stock Service - Get Stock Price: {symbol}"
    )

    return provider.get_stock_price(symbol)


def get_company_profile(symbol: str):

    logger.info(
        f"Stock Service - Get Company Profile: {symbol}"
    )

    return provider.get_company_profile(symbol)


def get_multiple_stocks(symbols: list):

    logger.info(
        f"Stock Service - Get Multiple Stocks: {symbols}"
    )

    stocks = []
    failed = []

    for symbol in symbols:

        data = provider.get_stock_price(symbol)

        if data:
            stocks.append(data)
        else:
            failed.append(symbol)

    return {
        "total": len(stocks),
        "data": stocks
    }