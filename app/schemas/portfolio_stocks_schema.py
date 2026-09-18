from pydantic import BaseModel


class PortfolioStockData(BaseModel):
    id: int
    code: str
    name: str
    sector: str
    subSector: str


class PortfolioStocksResponse(BaseModel):
    status: str
    message: str
    page: int
    limit: int
    totalPage: int
    totalData: int
    data: list[PortfolioStockData]