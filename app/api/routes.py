from fastapi import APIRouter, HTTPException, Query

from app.services.yahoo_service import (
    get_company_profile,
    get_multiple_stocks,
    get_stock_price,
)

from app.schemas.stock_schema import StockResponse
from app.schemas.multiple_stock_schema import MultipleStockResponse
from app.schemas.company_schema import CompanyResponse
from app.schemas.health_schema import HealthResponse

from app.utils.logger import logger

router = APIRouter()


# ===========================
# Home
# ===========================

@router.get("/", tags=["Home"])
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
    summary="Get Stock Price",
    description="Mengambil data harga saham berdasarkan simbol."
)
def stock(symbol: str):

    logger.info(f"REST Request - Stock: {symbol}")

    data = get_stock_price(symbol)

    if data is None:

        logger.warning(f"Stock not found: {symbol}")

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

    logger.info(f"REST Request - Multiple Stocks: {symbols}")

    symbol_list = [
        symbol.strip().upper()
        for symbol in symbols.split(",")
    ]

    data = get_multiple_stocks(symbol_list)

    if data["total"] == 0:

        logger.warning("No stock data found.")

        raise HTTPException(
            status_code=404,
            detail="No stock data found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        **data
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

    logger.info(f"REST Request - Company: {symbol}")

    data = get_company_profile(symbol)

    if data is None:

        logger.warning(f"Company not found: {symbol}")

        raise HTTPException(
            status_code=404,
            detail=f"Company '{symbol}' not found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "data": data
    }