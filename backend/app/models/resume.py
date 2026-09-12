from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(String, nullable=False)

    extracted_text = Column(Text, nullable=False)