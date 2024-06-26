from sqlalchemy import Column, Integer, String, Date, Float
from .database import Base

class ProcessedImage(Base):
    __tablename__ = 'processed_images'
    id = Column(Integer, primary_key=True, index=True)
    date_processed = Column(Date, index=True)
    cloud_coverage = Column(Float)
    image_path = Column(String, unique=True, index=True)
    classification_result = Column(String)
    evaluation_metric = Column(Float)
