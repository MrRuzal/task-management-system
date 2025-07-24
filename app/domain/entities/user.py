from dataclasses import dataclass
from app.domain.entities.common import EntityId


@dataclass
class User:
    id: EntityId
    username: str
    email: str
    hashed_password: str
    is_active: bool
