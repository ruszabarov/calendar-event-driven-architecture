from sqlalchemy import Column, String
from database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(String, primary_key=True, index=True)
    meeting_id = Column(String, index=True)
    url = Column(String(2000))
