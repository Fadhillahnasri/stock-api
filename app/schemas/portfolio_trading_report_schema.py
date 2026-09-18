from pydantic import BaseModel


class TradingReportSummary(BaseModel):
    quantity: int
    netAmount: float
    marketValue: float
    potentialGainLoss: float
    realizedGainLoss: float
    nettGainLoss: float


class TradingDealerSummary(BaseModel):
    dealerCode: str
    dealerName: str
    quantity: int
    netAmount: float
    marketValue: float
    potentialGainLoss: float
    realizedGainLoss: float
    nettGainLoss: float
    hasPosition: bool
    shouldDisplay: bool


class TradingReportData(BaseModel):
    dealerCode: str
    dealerName: str
    stockCode: str
    initialBuy: str
    buyId: int
    quantity: int
    price: str
    netAmount: str
    closingPrice: str
    marketValue: str
    unrealizedgainorloss: str
    unrealizedgainorlosspercentage: str
    holdingStartDate: str
    holdingDays: int
    holdingBusinessDays: int
    isExtended: bool


class PortfolioTradingReportResponse(BaseModel):
    status: str
    message: str
    page: int
    limit: int
    totalPage: int
    totalData: int
    summary: TradingReportSummary
    dealerSummaries: list[TradingDealerSummary]
    data: list[TradingReportData]