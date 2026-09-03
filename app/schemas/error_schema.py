from pydantic import BaseModel


class ErrorResponse(BaseModel):

    success: bool
    status: int
    message: str
    path: str