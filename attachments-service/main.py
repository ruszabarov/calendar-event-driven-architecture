

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine


from models import Meeting, Attachment

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get Attachments by IDs
@app.get("/attachments", response_model=List[schemas.Attachment])
def get_attachments(
        ids: Optional[str] = Query(None, description="Comma-separated list of attachment IDs"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Retrieve attachments. If `ids` are provided, filter by those IDs.
    Otherwise, return attachments with pagination.
    """
    if ids:
        ids_list = ids.split(",")
        attachments = crud.get_attachments_by_ids(db, ids_list)
    else:
        attachments = crud.get_attachments(db, skip=skip, limit=limit)
    return attachments


# Create Attachment with ID
@app.post("/attachments/{id}", response_model=schemas.Attachment)
def create_attachment_with_id(
        id: str,
        attachment: schemas.AttachmentCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new attachment with a specific ID.
    """
    existing_attachment = crud.get_attachment(db, id)
    if existing_attachment:
        raise HTTPException(status_code=400, detail="Attachment with this ID already exists")

    db_attachment = crud.create_attachment(db, attachment)
    return db_attachment


# Create Attachment without IDs
@app.post("/attachments", response_model=schemas.Attachment)
def create_attachment(
        attachment: schemas.AttachmentCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new attachment without specifying an ID. The ID is auto-generated.
    """
    db_attachment = crud.create_attachment(db, attachment)
    return db_attachment


# Update Attachment
@app.put("/attachments/{id}", response_model=schemas.Attachment)
def update_attachment(
        id: str,
        attachment: schemas.AttachmentCreate,
        db: Session = Depends(get_db)
):
    """
    Update an existing attachment's details.
    """
    db_attachment = crud.update_attachment(db, id, attachment)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return db_attachment


# Delete Attachment
@app.delete("/attachments/{id}")
def delete_attachment(
        id: str,
        db: Session = Depends(get_db)
):
    """
    Delete an attachment by its ID.
    """
    success = crud.delete_attachment(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return {"detail": "Attachment deleted"}
