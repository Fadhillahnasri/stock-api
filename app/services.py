import yfinance as yf


def get_stock_price(symbol: str):
    """
    Mengambil data harga saham berdasarkan simbol.
    """

    try:
        stock = yf.Ticker(symbol.upper())
        info = stock.info

        if not info:
            return None

        return {
            "symbol": symbol.upper(),
            "company_name": info.get("longName"),
            "current_price": info.get("currentPrice"),
            "high": info.get("dayHigh"),
            "low": info.get("dayLow"),
            "open": info.get("open"),
            "previous_close": info.get("previousClose"),
            "change": info.get("regularMarketChange"),
            "change_percent": info.get("regularMarketChangePercent"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),
            "market_state": info.get("marketState")
        }

    except Exception as e:
        print(f"Error get_stock_price: {e}")
        return None


def get_multiple_stocks(symbols: list):

    stocks = []
    failed = []

    for symbol in symbols:

        data = get_stock_price(symbol)

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


def get_company_profile(symbol: str):

    try:

        stock = yf.Ticker(symbol.upper())
        info = stock.info

        if not info:
            return None

        return {
            "symbol": symbol.upper(),
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "currency": info.get("currency")
        }

    except Exception as e:
        print(f"Error get_company_profile: {e}")
        return None