from fastapi import APIRouter, HTTPException, Query

from app.services.stock_service import (
    get_stock_price,
    get_multiple_stocks,
    get_company_profile,
    get_historical_prices,
)

from app.services.portfolio_service import (
    get_closing_prices,
    get_portfolios,
    get_stocks,
    get_trading_report,
    get_transactions,
    get_index_report,
)

from app.schemas.stock_schema import StockResponse
from app.schemas.multiple_stock_schema import MultipleStockResponse
from app.schemas.company_schema import CompanyResponse
from app.schemas.health_schema import HealthResponse
from app.schemas.portfolio_index_schema import PortfolioIndexResponse
from app.schemas.portfolio_transaction_schema import (
    PortfolioTransactionResponse,
)
from app.schemas.portfolio_trading_report_schema import PortfolioTradingReportResponse
from app.services.portfolio_service import ( get_index_prices,)
from app.schemas.portfolio_closing_prices_schema import ClosingPriceResponse
from app.schemas.portfolio_stocks_schema import PortfolioStocksResponse
from app.schemas.portfolio_portfolios_schema import PortfolioResponse
from app.services.portfolio_analysis_service import get_portfolio_analysis
from app.schemas.portfolio_analysis_schema import PortfolioAnalysisResponse
from app.services.historical_analysis_service import (
    calculate_historical_returns,
)
from app.services.sensitivity_analysis_service import (
    get_stock_sensitivity,
)
from app.services.stress_test_service import (
    run_historical_stress_test,     
)

from app.services.historical_scenario_service import (
    get_historical_scenarios,
)
from app.services.historical_analysis_service import calculate_historical_returns
from app.services.macro_sensitivity_service import calculate_macro_sensitivity
from app.services.macro_service import (
    get_exchange_rate,
    get_bi_rate,
)
from app.services.bi_rate_sensitivity_service import (
    calculate_bi_rate_sensitivity,
)
from app.services.macro_service import get_oil_price
from app.services.oil_price_sensitivity_service import (
    calculate_oil_price_sensitivity
)
from app.utils.logger import logger


router = APIRouter()


# ===========================
# Home
# ===========================

@router.get(
    "/",
    tags=["Home"]
)
def home():

    logger.info("REST Request - Home")

    return {
        "application": "Indonesia Stock API",
        "status": "running",
        "provider": "Yahoo Finance",
        "version": "1.0.0",
        "documentation": "/docs"
    }


# ===========================
# Health Check
# ===========================

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"]
)
def health():

    logger.info("REST Request - Health Check")

    return {
        "status": "healthy",
        "message": "API is running"
    }


# ===========================
# Single Stock
# ===========================

@router.get(
    "/stock/{symbol}",
    response_model=StockResponse,
    tags=["Stocks"],
    summary="Get Single Stock",
    description="Mengambil data satu saham berdasarkan simbol."
)
def stock(symbol: str):

    logger.info(
        f"REST Request - Stock: {symbol}"
    )

    data = get_stock_price(symbol)

    if data is None:

        logger.warning(
            f"Stock not found: {symbol}"
        )

        raise HTTPException(
            status_code=404,
            detail=f"Stock '{symbol}' not found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "data": data
    }


# ===========================
# Multiple Stocks
# ===========================

@router.get(
    "/stocks",
    response_model=MultipleStockResponse,
    tags=["Stocks"],
    summary="Get Multiple Stocks",
    description="Mengambil data beberapa saham sekaligus."
)
def stocks(
    symbols: str = Query(
        ...,
        description="Contoh: BBCA.JK,BBRI.JK,BMRI.JK"
    )
):

    logger.info(
        f"REST Request - Multiple Stocks: {symbols}"
    )

    symbol_list = [
        symbol.strip().upper()
        for symbol in symbols.split(",")
        if symbol.strip()
    ]

    data = get_multiple_stocks(symbol_list)

    if data["total"] == 0:

        logger.warning(
            "No stock data found."
        )

        raise HTTPException(
            status_code=404,
            detail="No stock data found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "total": data["total"],
        "failed": data["failed"],
        "data": data["data"]
    }

# ===========================
# Company Profile
# ===========================

@router.get(
    "/company/{symbol}",
    response_model=CompanyResponse,
    tags=["Companies"],
    summary="Get Company Profile",
    description="Mengambil profil perusahaan berdasarkan simbol saham."
)
def company(symbol: str):

    logger.info(
        f"REST Request - Company: {symbol}"
    )

    data = get_company_profile(symbol)

    if data is None:

        logger.warning(
            f"Company not found: {symbol}"
        )

        raise HTTPException(
            status_code=404,
            detail=f"Company '{symbol}' not found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "data": data
    }

@router.get(
    "/stocks/{symbol}/history",
    tags=["Stock"],
    summary="Get Historical Stock Prices",
    description="Mengambil data historis harga saham dari provider."
)
def historical_stock_prices(
    symbol: str,
    period: str = Query(
        "1y",
        description="Periode data historis, contoh: 1mo, 3mo, 6mo, 1y, 5y"
    ),
    interval: str = Query(
        "1d",
        description="Interval data, contoh: 1d, 1wk, 1mo"
    )
):
    logger.info(
        f"REST Request - Historical Stock Prices: "
        f"{symbol}, period={period}, interval={interval}"
    )

    return get_historical_prices(
        symbol=symbol,
        period=period,
        interval=interval
    )

@router.get(
    "/stocks/{symbol}/history/returns",
    tags=["Stock"],
    summary="Get Historical Stock Returns",
    description="Menghitung daily return berdasarkan data historis harga saham."
)
def historical_stock_returns(
    symbol: str,
    period: str = Query(
        "1y",
        description="Periode data historis, contoh: 1mo, 3mo, 6mo, 1y"
    ),
    interval: str = Query(
        "1d",
        description="Interval data, contoh: 1d, 1wk, 1mo"
    )
):
    logger.info(
        f"REST Request - Historical Stock Returns: "
        f"{symbol}, period={period}, interval={interval}"
    )

    return calculate_historical_returns(
        symbol=symbol,
        period=period,
        interval=interval
    )

# ===========================
# Portfolio Transactions
# ===========================

@router.get(
    "/portfolio/transactions",
    response_model=PortfolioTransactionResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Transactions",
    description="Mengambil data transaksi portfolio dari Internal API."
)
def portfolio_transactions():

    logger.info(
        "REST Request - Portfolio Transactions"
    )

    params = {
        "page": 1,
        "limit": 20,
        "orderBy": "createdAt",
        "sort": "desc"
    }

    return get_transactions(params=params)

# ===========================
# Portfolio Index Report
# ===========================

@router.get(
    "/portfolio/index-report",
    response_model=PortfolioIndexResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Index Report",
    description="Mengambil laporan portfolio berdasarkan indeks dari Internal API."
)
def portfolio_index_report():

    logger.info(
        "REST Request - Portfolio Index Report"
    )

    return get_index_report()


@router.get(
    "/portfolio/trading-report",
    response_model=PortfolioTradingReportResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Trading Report",
    description="Mengambil data trading report portfolio dari Internal API."
)
def portfolio_trading_report():
    logger.info("REST Request - Portfolio Trading Report")

    params = {
        "page": 1,
        "limit": 20,
    }

    return get_trading_report(params=params)


@router.get(
    "/portfolio/index-prices",
    tags=["Portfolio"],
    summary="Get Portfolio Index Prices",
    description="Mengambil data harga indeks dari Internal API."
)
def portfolio_index_prices():
    logger.info("REST Request - Portfolio Index Prices")

    params = {
        "page": 1,
        "limit": 20,
        "orderBy": "indexCode",
        "sort": "asc"
    }

    return get_index_prices(params=params)

@router.get(
    "/portfolio/closing-prices",
    response_model=ClosingPriceResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Closing Prices",
    description="Mengambil data harga penutupan saham dari Internal API."
)
def portfolio_closing_prices(
    date: str = Query(
        ...,
        description="Tanggal closing price. Format: YYYY-MM-DD"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Nomor halaman"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Jumlah data per halaman"
    )
):
    logger.info(
        f"REST Request - Portfolio Closing Prices: "
        f"date={date}, page={page}, limit={limit}"
    )

    params = {
        "page": page,
        "limit": limit,
        "orderBy": "stockCode",
        "sort": "asc",
        "date": date
    }

    return get_closing_prices(params=params)

@router.get(
    "/portfolio/stocks",
    response_model=PortfolioStocksResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Stocks",
    description="Mengambil data saham dari Internal API."
)
def portfolio_stocks():
    logger.info("REST Request - Portfolio Stocks")

    params = {
        "page": 1,
        "limit": 20,
        "orderBy": "code",
        "sort": "asc"
    }

    return get_stocks(params=params)

@router.get(
    "/portfolio/portfolios",
    response_model=PortfolioResponse,
    tags=["Portfolio"],
    summary="Get Portfolio List",
    description="Mengambil daftar portfolio dari Internal API."
)
def portfolio_portfolios():
    logger.info("REST Request - Portfolio Portfolios")
    return get_portfolios()

@router.get("/portfolio/analysis")
def portfolio_analysis(date: str = Query(...)):
    logger.info(f"REST Request - Portfolio Analysis: {date}")

    try:
        return get_portfolio_analysis(date=date)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
def portfolio_analysis(
    date: str = Query(
        ...,
        description="Tanggal closing price. Format: YYYY-MM-DD"
    )
):
    logger.info(
        f"REST Request - Portfolio Analysis: {date}"
    )

    return get_portfolio_analysis(date=date)

@router.get(
    "/stocks/{symbol}/sensitivity",
    tags=["Stock"],
    summary="Get Stock Sensitivity",
    description="Menghitung sensitivitas historis saham terhadap benchmark.",
)
def stock_sensitivity(
    symbol: str,
    benchmark: str = Query(
        "^JKSE",
        description="Benchmark saham, default ^JKSE (IHSG).",
    ),
    period: str = Query(
        "1y",
        description="Periode data historis.",
    ),
    interval: str = Query(
        "1d",
        description="Interval data historis.",
    ),
):
    logger.info(
        f"REST Request - Stock Sensitivity: "
        f"{symbol} vs {benchmark}"
    )

    return get_stock_sensitivity(
        symbol=symbol,
        benchmark_symbol=benchmark,
        period=period,
        interval=interval,
    )

@router.get("/stress-test/historical")
def historical_stress_test(
    portfolioDate: str = Query(...),
    scenarioId: str = Query(...)
):
    logger.info(
        f"REST Request - Historical Stress Test: "
        f"portfolioDate={portfolioDate}, "
        f"scenarioId={scenarioId}"
    )

    result = run_historical_stress_test(
        portfolio_date=portfolioDate,
        scenario_id=scenarioId,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Historical stress test data tidak tersedia."
        )

    return result

@router.get("/stress-test/scenarios")
def historical_stress_test_scenarios():
    logger.info("REST Request - Historical Stress Test Scenarios")

    return get_historical_scenarios()

@router.get("/macro/exchange-rate")
def macro_exchange_rate(
    currency: str = Query("USD"),
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - Macro Exchange Rate: "
        f"{currency}, {startDate} to {endDate}"
    )

    try:
        return get_exchange_rate(
            currency=currency,
            start_date=startDate,
            end_date=endDate
        )

    except Exception as e:
        logger.exception(
            f"Macro Exchange Rate Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Gagal mengambil data exchange rate."
        )

@router.get("/macro/sensitivity")
def macro_sensitivity(
    symbol: str = Query(...),
    currency: str = Query("USD"),
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - Macro Sensitivity: "
        f"symbol={symbol}, "
        f"currency={currency}, "
        f"startDate={startDate}, "
        f"endDate={endDate}"
    )

    try:
        stock_data = calculate_historical_returns(
            symbol=symbol,
            period="max",
            interval="1d"
        )

        if not stock_data or not stock_data.get("data"):
            raise HTTPException(
                status_code=404,
                detail=f"Historical data untuk {symbol} tidak tersedia."
            )

        macro_data = get_exchange_rate(
            currency=currency,
            start_date=startDate,
            end_date=endDate
        )

        if not macro_data or not macro_data.get("data"):
            raise HTTPException(
                status_code=404,
                detail=f"Macro data untuk {currency}/IDR tidak tersedia."
            )

        sensitivity = calculate_macro_sensitivity(
            stock_data=stock_data["data"],
            macro_data=macro_data["data"]
        )

        if sensitivity is None:
            raise HTTPException(
                status_code=404,
                detail="Data tidak cukup untuk menghitung macro sensitivity."
            )

        return {
            "symbol": symbol.upper(),
            "macro": macro_data["indicator"],
            "source": macro_data["source"],
            "sensitivity": sensitivity
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Macro Sensitivity Error: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Gagal menghitung macro sensitivity."
        )

@router.get("/macro/bi-rate")
def macro_bi_rate(
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - BI-Rate: "
        f"startDate={startDate}, endDate={endDate}"
    )

    try:
        result = get_bi_rate(
            start_date=startDate,
            end_date=endDate
        )

        if not result or not result.get("data"):
            raise HTTPException(
                status_code=404,
                detail="Data BI-Rate tidak tersedia."
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"BI-Rate Error: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Gagal mengambil data BI-Rate."
        )
@router.get("/macro/bi-rate/sensitivity")
def macro_bi_rate_sensitivity(
    symbol: str = Query(...),
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - BI-Rate Sensitivity: "
        f"symbol={symbol}, "
        f"startDate={startDate}, "
        f"endDate={endDate}"
    )

    try:
        bi_rate_data = get_bi_rate(
            start_date=startDate,
            end_date=endDate
        )

        if not bi_rate_data or not bi_rate_data.get("data"):
            raise HTTPException(
                status_code=404,
                detail="Data BI-Rate tidak tersedia."
            )

        result = calculate_bi_rate_sensitivity(
            symbol=symbol,
            start_date=startDate,
            end_date=endDate,
            bi_rate_data=bi_rate_data["data"]
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Data sensitivity BI-Rate untuk "
                    f"{symbol} tidak tersedia."
                )
            )

        return {
            "symbol": result["symbol"],
            "macro": result["macro"],
            "source": "Bank Indonesia",
            "observations": result["observations"],
            "startDate": result["startDate"],
            "endDate": result["endDate"],
            "events": result["events"],
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"BI-Rate Sensitivity Error: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail="Gagal menghitung BI-Rate sensitivity."
        )

@router.get("/macro/oil-price")
def macro_oil_price(
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - Oil Price: "
        f"startDate={startDate}, endDate={endDate}"
    )

    try:
        result = get_oil_price(
            start_date=startDate,
            end_date=endDate
        )

        if not result or not result.get("data"):
            raise HTTPException(
                status_code=404,
                detail="Data WTI Oil Price tidak tersedia."
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Oil Price Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Gagal mengambil data WTI Oil Price."
        )


@router.get("/macro/oil-price/sensitivity")
def macro_oil_price_sensitivity(
    symbol: str = Query(...),
    startDate: str = Query(...),
    endDate: str = Query(...)
):
    logger.info(
        f"REST Request - Oil Price Sensitivity: "
        f"symbol={symbol}, "
        f"startDate={startDate}, "
        f"endDate={endDate}"
    )

    try:
        stock_data = calculate_historical_returns(
            symbol=symbol,
            period="max",
            interval="1d"
        )

        if not stock_data or not stock_data.get("data"):
            raise HTTPException(
                status_code=404,
                detail=f"Data historis untuk {symbol} tidak tersedia."
            )

        oil_data = get_oil_price(
            start_date=startDate,
            end_date=endDate
        )

        if not oil_data or not oil_data.get("data"):
            raise HTTPException(
                status_code=404,
                detail="Data WTI Oil Price tidak tersedia."
            )

        sensitivity = calculate_oil_price_sensitivity(
            stock_data=stock_data["data"],
            oil_data=oil_data["data"]
        )

        if sensitivity is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Data sensitivity Oil Price untuk "
                    f"{symbol} tidak tersedia."
                )
            )

        return {
            "symbol": symbol.strip().upper(),
            "macro": "WTI Oil Price",
            "source": "U.S. Energy Information Administration",
            "unit": "USD/barrel",
            "sensitivity": sensitivity
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Oil Price Sensitivity Error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Gagal menghitung Oil Price sensitivity."
        )