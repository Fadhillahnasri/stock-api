from app.schemas.portfolio_portfolios_schema import (
    PortfolioData,
    PortfolioResponse,
)


def test_portfolio_data_schema():
    data = PortfolioData(
        code="DPBNI",
        name="Index dan Trading",
        category="INTERNAL",
        isActive=True,
    )

    assert data.code == "DPBNI"
    assert data.name == "Index dan Trading"
    assert data.category == "INTERNAL"
    assert data.isActive is True


def test_portfolio_response_schema():
    response = PortfolioResponse(
        status="success",
        data=[
            {
                "code": "BNP",
                "name": "Saham MI BNP",
                "category": "EXTERNAL",
                "isActive": True,
            },
            {
                "code": "DPBNI",
                "name": "Index dan Trading",
                "category": "INTERNAL",
                "isActive": True,
            },
        ],
    )

    assert response.status == "success"
    assert len(response.data) == 2
    assert response.data[0].code == "BNP"
    assert response.data[1].category == "INTERNAL"