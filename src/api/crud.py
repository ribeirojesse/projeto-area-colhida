from sqlalchemy.orm import Session
from . import models, schemas

def get_images(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ProcessedImage).offset(skip).limit(limit).all()

def get_image_by_id(db: Session, image_id: int):
    return db.query(models.ProcessedImage).filter(models.ProcessedImage.id == image_id).first()


def create_image(db: Session, image: schemas.ProcessedImageCreate):
    db_image = models.ProcessedImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_images_by_date_and_cloud_coverage(db: Session, date_processed: str = None, cloud_coverage: float = None, skip: int = 0, limit: int = 10):
    query = db.query(models.ProcessedImage)
    if date_processed:
        query = query.filter(models.ProcessedImage.date_processed == date_processed)
    if cloud_coverage is not None:
        query = query.filter(models.ProcessedImage.cloud_coverage <= cloud_coverage)
    return query.offset(skip).limit(limit).all()
