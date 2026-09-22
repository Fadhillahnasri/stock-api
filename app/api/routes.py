from fastapi import APIRouter, HTTPException, Query

from app.services.stock_service import (
    get_stock_price,
    get_multiple_stocks,
    get_company_profile,
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

@router.get(
    "/portfolio/analysis",
    response_model=PortfolioAnalysisResponse,
    tags=["Portfolio"],
    summary="Get Portfolio Analysis",
    description="Menghitung analisis kinerja portfolio berdasarkan index report."
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