import pytest
from app.schemas.stock_schema import StockData


def test_stock_data_schema():
    stock = StockData(
        symbol="BBCA.JK",
        company_name="PT Bank Central Asia Tbk",
        current_price=9000,
        high=9100,
        low=8900,
        open=8950,
        previous_close=8950,
        change=50,
        change_percent=0.56
    )

    assert stock.symbol == "BBCA.JK"
    assert stock.company_name == "PT Bank Central Asia Tbk"
    assert stock.current_price == 9000
    assert stock.change == 50
    assert stock.change_percent == 0.56


def test_stock_data_invalid_symbol():
    with pytest.raises(ValueError):
        StockData(
            symbol=123,
            company_name="PT Bank Central Asia Tbk",
            current_price=9000,
            high=9100,
            low=8900,
            open=8950,
            previous_close=8950,
            change=50,
            change_percent=0.56
        )