from app.providers.yahoo_provider import YahooProvider
from app.utils.logger import logger


# Provider yang digunakan aplikasi
provider = YahooProvider()


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
        "total_requested": len(symbols),
        "success": len(stocks),
        "failed": failed,
        "data": stocks
    }