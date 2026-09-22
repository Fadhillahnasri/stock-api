from app.schemas.portfolio_analysis_schema import (
    PortfolioStockAnalysis,
    PortfolioAnalysisResponse,
)


def test_portfolio_stock_analysis_schema():
    data = {
        "stockCode": "BBCA",
        "costBasis": 100000000,
        "marketValue": 90000000,
        "unrealizedGainLoss": -10000000,
        "performancePercentage": -10,
        "portfolioWeight": 15,
    }

    result = PortfolioStockAnalysis(**data)

    assert result.stockCode == "BBCA"
    assert result.costBasis == 100000000
    assert result.marketValue == 90000000


def test_portfolio_analysis_response_schema():
    stock = {
        "stockCode": "BBCA",
        "costBasis": 100000000,
        "marketValue": 90000000,
        "unrealizedGainLoss": -10000000,
        "performancePercentage": -10,
        "portfolioWeight": 15,
    }

    data = {
        "totalCostBasis": 100000000,
        "totalMarketValue": 90000000,
        "totalUnrealizedGainLoss": -10000000,
        "totalUnrealizedGainLossPercentage": -10,
        "stocks": [stock],
        "topGainers": [stock],
        "topLosers": [stock],
    }

    result = PortfolioAnalysisResponse(**data)

    assert result.totalCostBasis == 100000000
    assert len(result.stocks) == 1
    assert result.stocks[0].stockCode == "BBCA"