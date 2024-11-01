# schemas.py

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import uuid


class AttachmentBase(BaseModel):
    meetingId: Optional[str]
    url: HttpUrl

    class Config:
        orm_mode = True


class AttachmentCreate(AttachmentBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        orm_mode = True


class Attachment(AttachmentBase):
    id: str

    class Config:
        orm_mode = True
