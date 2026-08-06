from fastapi import APIRouter, HTTPException, Query

from app.services.yahoo_service import (
    get_company_profile,
    get_multiple_stocks,
    get_stock_price,
)
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

@router.get("/health", tags=["Health"])
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

    if not data:
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