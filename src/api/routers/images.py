from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database

router = APIRouter()

@router.post("/images/", response_model=schemas.ProcessedImage)
def create_image(image: schemas.ProcessedImageCreate, db: Session = Depends(database.get_db)):
    return crud.create_image(db=db, image=image)

@router.get("/images/", response_model=List[schemas.ProcessedImage])
def read_images(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    return images

@router.get("/images/{image_id}", response_model=schemas.ProcessedImage)
def read_image(image_id: int, db: Session = Depends(database.get_db)):
    db_image = crud.get_image_by_id(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.get("/images/search/", response_model=List[schemas.ProcessedImage])
def search_images(date_processed: Optional[str] = None, cloud_coverage: Optional[float] = None, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    images = crud.get_images_by_date_and_cloud_coverage(db, date_processed, cloud_coverage, skip, limit)
    return images
