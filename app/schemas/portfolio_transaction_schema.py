from pydantic import BaseModel
from typing import Optional


class PortfolioTransactionData(BaseModel):
    id: int
    transactionDate: str
    dealerId: int
    dealerCode: str
    stockId: int
    stockCode: str
    transactionType: str
    quantity: int
    price: str
    investmentType: str
    brokerId: int
    brokerCode: str
    brokerName: str
    isPPHIncluded: bool

    fee: Optional[str] = None
    totalValue: Optional[str] = None
    pph23Amount: Optional[str] = None
    netAmount: str
    netSettlement: Optional[str] = None

    createdBy: Optional[str] = None
    createdAt: str
    updatedAt: str


class PortfolioTransactionDataResponse(BaseModel):
    total: int
    page: int
    limit: int
    totalPage: int
    data: list[PortfolioTransactionData]


class PortfolioTransactionResponse(BaseModel):
    status: str
    message: str
    data: PortfolioTransactionDataResponse