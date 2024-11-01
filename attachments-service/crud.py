

from sqlalchemy.orm import Session
import models
import schemas
import uuid
from typing import List, Optional


def get_attachment(db: Session, attachment_id: str) -> Optional[models.Attachment]:
    """
    Retrieve a single attachment by its ID.
    """
    return db.query(models.Attachment).filter(models.Attachment.id == attachment_id).first()


def get_attachments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Attachment]:
    """
    Retrieve a list of attachments with pagination.
    """
    return db.query(models.Attachment).offset(skip).limit(limit).all()


def get_attachments_by_ids(db: Session, ids: List[str]) -> List[models.Attachment]:
    """
    Retrieve multiple attachments by their IDs.
    """
    return db.query(models.Attachment).filter(models.Attachment.id.in_(ids)).all()


def create_attachment(db: Session, attachment: schemas.AttachmentCreate) -> models.Attachment:
    """
    Create a new attachment.
    """
    db_attachment = models.Attachment(
        id=attachment.id or str(uuid.uuid4()),
        meetingId=attachment.meetingId,
        url=str(attachment.url),
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def update_attachment(db: Session, attachment_id: str, attachment: schemas.AttachmentCreate) -> Optional[models.Attachment]:
    """
    Update an existing attachment.
    """
    db_attachment = get_attachment(db, attachment_id)
    if not db_attachment:
        return None

    db_attachment.meetingId = attachment.meetingId or db_attachment.meetingId
    db_attachment.url = str(attachment.url) if attachment.url else db_attachment.url

    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def delete_attachment(db: Session, attachment_id: str) -> bool:
    """
    Delete an attachment by its ID.
    """
    db_attachment = get_attachment(db, attachment_id)
    if not db_attachment:
        return False

    db.delete(db_attachment)
    db.commit()
    return True
