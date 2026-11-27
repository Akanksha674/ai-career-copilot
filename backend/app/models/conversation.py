from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False,
        default="New Conversation"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )