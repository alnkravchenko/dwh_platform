from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ValidationError
from services.query import QueryService


class QueryModel(BaseModel):
    project_id: UUID
    query: str

    @classmethod
    def validate_query(
        cls, query: QueryModel, query_service: QueryService, **kwargs
    ) -> bool:
        """
        Raises error if query is invalid
        """
        is_valid, msg = query_service.validate_query(query.project_id, query.query)
        if not is_valid:
            log = kwargs["logger"]
            prefix = kwargs["prefix"]
            log.info(f"{prefix} 400 {msg}")
            raise ValidationError(f"Invalid query. {msg}")  # type: ignore
        return True


class QueryWrite(BaseModel):
    project_id: UUID
    query: Optional[str]
