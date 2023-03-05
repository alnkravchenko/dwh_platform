from pydantic import BaseModel


class DefaultResponse(BaseModel):
    details: str
