from app.schemas.portfolio_closing_prices_schema import (
    ClosingPriceData,
    ClosingPriceResponse,
)


def test_closing_price_data_schema():
    data = ClosingPriceData(
        stockCode="AADI",
        stockName="Adaro Andalan Indonesia Tbk",
        closingPrice=8325,
    )

    assert data.stockCode == "AADI"
    assert data.stockName == "Adaro Andalan Indonesia Tbk"
    assert data.closingPrice == 8325


def test_closing_price_response_schema():
    response = ClosingPriceResponse(
        status="success",
        message="Successfully retrieve data closing prices",
        page=1,
        limit=20,
        totalPage=48,
        totalData=959,
        data=[
            {
                "stockCode": "AADI",
                "stockName": "Adaro Andalan Indonesia Tbk",
                "closingPrice": 8325,
            }
        ],
    )

    assert response.status == "success"
    assert response.page == 1
    assert response.limit == 20
    assert response.totalPage == 48
    assert response.totalData == 959
    assert len(response.data) == 1
    assert response.data[0].stockCode == "AADI"