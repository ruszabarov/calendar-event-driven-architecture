from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import uuid


class AttachmentBase(BaseModel):
    meetingId: Optional[str]
    url: HttpUrl

    class Config:
        from_attributes = True


class AttachmentCreate(AttachmentBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True


class Attachment(AttachmentBase):
    id: str

    class Config:
        from_attributes = True


class AttachmentCreateWithoutId(BaseModel):
    name: str
    file_url: str

    class Config:
        from_attributes = True
