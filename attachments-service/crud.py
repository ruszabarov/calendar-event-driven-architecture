
from sqlalchemy.orm import Session
import models
import schemas
import uuid

def create_attachment(db: Session, attachment: schemas.AttachmentCreate):
    db_attachment = models.Attachment(
        id=attachment.id or str(uuid.uuid4()),
        meetingId=attachment.meetingId,
        url=str(attachment.url),
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

# Add other CRUD functions as needed
