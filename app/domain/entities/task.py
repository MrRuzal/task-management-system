from dataclasses import dataclass
from datetime import date
from app.domain.entities.common import EntityId


@dataclass
class Task:
    id: EntityId
    title: str
    due_date: date
    user_id: int
    description: str | None = None
