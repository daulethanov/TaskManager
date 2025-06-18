from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, ForeignKey, String, Enum, UUID
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.features.task.models.associations import task_tags
from src.features.task.models.tag import Tag


class TaskStatus(PyEnum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    overdue = "overdue"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.new)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")

    tags = relationship(Tag, secondary=task_tags, back_populates="tasks")

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < datetime.utcnow() and self.status != TaskStatus.done

