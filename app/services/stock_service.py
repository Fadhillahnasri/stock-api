from app.providers.yahoo_provider import (
    fetch_stock,
    fetch_company
)

from app.utils.logger import logger


def get_stock(symbol: str):

    logger.info(f"Service - Get Stock: {symbol}")

    return fetch_stock(symbol)


def get_company(symbol: str):

    logger.info(f"Service - Get Company: {symbol}")

    return fetch_company(symbol)


def get_multiple_stocks(symbols: list[str]):

    logger.info("Service - Get Multiple Stocks")

    stocks = []
    failed = []

    for symbol in symbols:

        data = get_stock(symbol)

        if data:

            stocks.append(data)

        else:

            failed.append(symbol)

    return {

        "total": len(stocks),

        "failed": failed,

        "data": stocks
    }