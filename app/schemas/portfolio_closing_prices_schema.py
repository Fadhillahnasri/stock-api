from pydantic import BaseModel


class ClosingPriceData(BaseModel):
    stockCode: str
    stockName: str
    closingPrice: float


class ClosingPriceResponse(BaseModel):
    status: str
    message: str
    page: int
    limit: int
    totalPage: int
    totalData: int
    data: list[ClosingPriceData]