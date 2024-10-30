from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import uuid


class AttachmentBase(BaseModel):
    meeting_id: str
    url: HttpUrl


class AttachmentCreate(AttachmentBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))


class AttachmentCreateWithoutId(AttachmentBase):
    pass


class Attachment(AttachmentBase):
    id: str

    class Config:
        orm_mode = True
