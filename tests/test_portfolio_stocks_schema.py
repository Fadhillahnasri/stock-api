from app.schemas.portfolio_stocks_schema import (
    PortfolioStockData,
    PortfolioStocksResponse,
)


def test_portfolio_stock_data_schema():
    data = PortfolioStockData(
        id=933,
        code="AADI",
        name="Adaro Andalan Indonesia Tbk",
        sector="Energi",
        subSector="Minyak, Gas & Batu Bara",
    )

    assert data.id == 933
    assert data.code == "AADI"
    assert data.name == "Adaro Andalan Indonesia Tbk"
    assert data.sector == "Energi"
    assert data.subSector == "Minyak, Gas & Batu Bara"


def test_portfolio_stocks_response_schema():
    response = PortfolioStocksResponse(
        status="success",
        message="Successfully retrieve data stocks",
        page=1,
        limit=20,
        totalPage=49,
        totalData=967,
        data=[
            {
                "id": 933,
                "code": "AADI",
                "name": "Adaro Andalan Indonesia Tbk",
                "sector": "Energi",
                "subSector": "Minyak, Gas & Batu Bara",
            }
        ],
    )

    assert response.status == "success"
    assert response.page == 1
    assert response.limit == 20
    assert response.totalPage == 49
    assert response.totalData == 967
    assert len(response.data) == 1
    assert response.data[0].code == "AADI"