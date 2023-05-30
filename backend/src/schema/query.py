from uuid import UUID

from pydantic import BaseModel


class QueryModel(BaseModel):
    project_id: UUID
    query: str
