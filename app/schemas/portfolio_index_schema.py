from pydantic import BaseModel
from typing import Optional


class PortfolioIndexData(BaseModel):
    stockCode: str
    indexes: str
    initialBuy: str
    quantity: str
    netAmount: str
    price: str
    closingPrice: str
    marketValue: str
    unrealizedgainorloss: str
    unrealizedgainorlosspercentage: str
    benchmarklq45: Optional[str] = None
    benchmarkidx80: Optional[str] = None
    portfolioWeight: float
    portfolioWeightPercentage: float
    lq45PositionStatus: str
    idx80PositionStatus: str


class PortfolioIndexSummary(BaseModel):
    totalMarketValue: float


class PortfolioIndexResponse(BaseModel):
    status: str
    message: str
    page: int
    limit: int
    totalPage: int
    totalData: int
    summary: PortfolioIndexSummary
    data: list[PortfolioIndexData]