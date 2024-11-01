# models.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)

    attachments = relationship("Attachment", back_populates="meeting")


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    meetingId = Column(String, ForeignKey("meetings.id"), nullable=True)
    url = Column(String, nullable=False)


    meeting = relationship("Meeting", back_populates="attachments")
