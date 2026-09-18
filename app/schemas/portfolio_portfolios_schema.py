from pydantic import BaseModel


class PortfolioData(BaseModel):
    code: str
    name: str
    category: str
    isActive: bool


class PortfolioResponse(BaseModel):
    status: str
    data: list[PortfolioData]