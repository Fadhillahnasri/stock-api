import pytest

from app.schemas.multiple_stock_schema import (
    StockItem,
    MultipleStockResponse
)


def test_multiple_stock_response_schema():
    response = MultipleStockResponse(
        success=True,
        provider="Yahoo Finance",
        total=2,
        failed=["ABC123.JK"],
        data=[
            StockItem(
                symbol="BBCA.JK",
                company_name="PT Bank Central Asia Tbk",
                current_price=9000,
                high=9100,
                low=8900,
                open=8950,
                previous_close=8950,
                change=50,
                change_percent=0.56
            ),
            StockItem(
                symbol="BBRI.JK",
                company_name="PT Bank Rakyat Indonesia (Persero) Tbk",
                current_price=4500,
                high=4550,
                low=4450,
                open=4480,
                previous_close=4480,
                change=20,
                change_percent=0.45
            )
        ]
    )

    assert response.success is True
    assert response.provider == "Yahoo Finance"
    assert response.total == 2
    assert response.failed == ["ABC123.JK"]
    assert len(response.data) == 2
    assert response.data[0].symbol == "BBCA.JK"
    assert response.data[1].symbol == "BBRI.JK"


def test_multiple_stock_invalid_total():
    with pytest.raises(ValueError):
        MultipleStockResponse(
            success=True,
            provider="Yahoo Finance",
            total="invalid",
            failed=[],
            data=[]
        )