from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine

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
        ids: Optional[str] = Query(None),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    if ids:
        ids_list = ids.split(",")
        attachments = crud.get_attachments_by_ids(db, ids_list)
    else:
        attachments = crud.get_attachments(db, skip=skip, limit=limit)
    return attachments


# Create Attachment
@app.post("/attachments/{id}", response_model=schemas.Attachment)
def create_attachment_with_id(
        id: str,
        attachment: schemas.AttachmentCreateWithoutId,
        db: Session = Depends(get_db)
):
    existing_attachment = crud.get_attachment(db, id)
    if existing_attachment:
        raise HTTPException(status_code=400, detail="Attachment with this ID already exists")

    new_attachment = schemas.AttachmentCreate(
        id=id,
        url=attachment.url,
    )
    db_attachment = crud.create_attachment(db, new_attachment)

    return db_attachment


# Create Attachment without IDs
@app.post("/attachments", response_model=schemas.Attachment)
def create_attachment(
        attachment: schemas.AttachmentCreateWithoutId,
        db: Session = Depends(get_db)
):
    new_attachment = schemas.AttachmentCreate(
        url=attachment.url,
    )
    db_attachment = crud.create_attachment(db, new_attachment)
    return db_attachment


# Update Attachment
@app.put("/attachments/{id}", response_model=schemas.Attachment)
def update_attachment(
        id: str,
        attachment: schemas.AttachmentCreateWithoutId,
        db: Session = Depends(get_db)
):
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
    db_attachment = crud.get_attachment(db, id)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    crud.delete_attachment(db, id)
    return {"detail": "Attachment deleted"}
