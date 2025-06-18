from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from src.features.task.models.task import TaskStatus


class CreateTaskSchema(BaseModel):
    title: str
    description: Optional[str]
    status: str
    due_date: datetime
    tags: Optional[List]

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        valid_values = {status.value for status in TaskStatus}
        if value not in valid_values:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_values)}")
        return value


class TagSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TaskSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[datetime]
    tags: List[TagSchema] = []

    model_config = ConfigDict(from_attributes=True)


class UpdateTaskSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)