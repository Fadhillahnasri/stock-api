from fastapi import APIRouter, HTTPException, Query

from app.services import (
    get_stock_price,
    get_multiple_stocks,
    get_company_profile
)

router = APIRouter()


@router.get("/", tags=["Home"])
def home():
    return {
        "application": "Indonesia Stock API",
        "provider": "Yahoo Finance",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@router.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "message": "API is running"
    }


@router.get(
    "/stock/{symbol}",
    tags=["Stocks"],
    summary="Get Stock Price",
    description="Mengambil data harga saham berdasarkan simbol."
)
def stock(symbol: str):

    data = get_stock_price(symbol)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Stock '{symbol}' not found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "data": data
    }


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

    symbol_list = [
        s.strip().upper()
        for s in symbols.split(",")
    ]

    data = get_multiple_stocks(symbol_list)

    return {
        "success": True,
        "provider": "Yahoo Finance",
        **data
    }


@router.get(
    "/company/{symbol}",
    tags=["Company"],
    summary="Get Company Profile",
    description="Mengambil profil perusahaan berdasarkan simbol saham."
)
def company(symbol: str):

    data = get_company_profile(symbol)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{symbol}' not found."
        )

    return {
        "success": True,
        "provider": "Yahoo Finance",
        "data": data
    }