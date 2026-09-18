from app.providers.internal_provider import InternalProvider
from app.utils.logger import logger

provider = InternalProvider()


def get_portfolios():
    logger.info("Portfolio Service - Get Portfolios")
    return provider.get_portfolios()

def get_stocks():
    logger.info("Portfolio Service - Get Stocks")
    return provider.get_stocks()

def get_closing_prices(params: dict | None = None):
    logger.info("Portfolio Service - Get Closing Prices")
    return provider.get_closing_prices(params=params)

def get_index_prices(params: dict | None = None):
    logger.info("Portfolio Service - Get Index Prices")
    return provider.get_index_prices(params=params)

def get_index_report(params: dict | None = None):
    logger.info("Portfolio Service - Get Index Report")
    return provider.get_index_report(params=params)

def get_trading_report(params: dict | None = None):
    logger.info("Portfolio Service - Get Trading Report")
    return provider.get_trading_report(params=params)

def get_transactions(params: dict | None = None):
    logger.info("Portfolio Service - Get Transactions")
    return provider.get_transactions(params=params)



