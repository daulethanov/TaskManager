from datetime import datetime

import bcrypt
from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.features.task.models.task import Task


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tasks = relationship(Task, back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def generate_password_hash(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password_hash: str):
        return bcrypt.checkpw(password_hash.encode('utf-8'), self.password_hash.encode('utf-8'))