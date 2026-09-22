from pydantic import BaseModel


class PortfolioStockAnalysis(BaseModel):
    stockCode: str
    costBasis: float
    marketValue: float
    unrealizedGainLoss: float
    performancePercentage: float
    portfolioWeight: float
    closingPrice: float


class PortfolioAnalysisResponse(BaseModel):
    totalCostBasis: float
    totalMarketValue: float
    totalUnrealizedGainLoss: float
    totalUnrealizedGainLossPercentage: float
    stocks: list[PortfolioStockAnalysis]
    topGainers: list[PortfolioStockAnalysis]
    topLosers: list[PortfolioStockAnalysis]