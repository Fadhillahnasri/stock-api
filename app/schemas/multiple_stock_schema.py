from pydantic import BaseModel


class StockItem(BaseModel):

    symbol: str
    company_name: str
    current_price: float | None
    high: float | None
    low: float | None
    open: float | None
    previous_close: float | None
    change: float | None
    change_percent: float | None


class MultipleStockResponse(BaseModel):

    success: bool
    provider: str
    total: int
    data: list[StockItem]