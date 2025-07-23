from pydantic import BaseModel
from datetime import date


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: date


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    due_date: date


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    due_date: date
    user_id: int

    class Config:
        from_attributes = True
