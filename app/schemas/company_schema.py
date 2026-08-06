from pydantic import BaseModel


class CompanyData(BaseModel):

    symbol: str
    company_name: str
    exchange: str | None
    sector: str | None
    industry: str | None
    website: str | None


class CompanyResponse(BaseModel):

    success: bool
    provider: str
    data: CompanyData