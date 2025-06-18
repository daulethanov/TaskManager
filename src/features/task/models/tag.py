from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.features.task.models.associations import task_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")
