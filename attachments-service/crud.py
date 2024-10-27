from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import uuid


def get_attachment(db: Session, id: str):
    return db.query(models.Attachment).filter(models.Attachment.id == id).first()


def get_attachments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attachment).offset(skip).limit(limit).all()


def get_attachments_by_ids(db: Session, ids: List[str]):
    return db.query(models.Attachment).filter(models.Attachment.id.in_(ids)).all()


def create_attachment(db: Session, attachment: schemas.AttachmentCreate):
    db_attachment = models.Attachment(
        id=attachment.id or str(uuid.uuid4()),
        url=str(attachment.url),
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def delete_attachment(db: Session, id: str):
    db_attachment = get_attachment(db, id)
    if db_attachment:
        db.delete(db_attachment)
        db.commit()
        return True
    return False


def update_attachment(db: Session, id: str, attachment: schemas.AttachmentCreateWithoutId):
    db_attachment = get_attachment(db, id)
    if db_attachment:
        db_attachment.url = str(attachment.url)
        db.commit()
        db.refresh(db_attachment)
        return db_attachment
    return None
