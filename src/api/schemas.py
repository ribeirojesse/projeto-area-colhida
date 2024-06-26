from pydantic import BaseModel
from datetime import date

class ProcessedImageBase(BaseModel):
    date_processed: date 
    cloud_coverage: float
    image_path: str
    classification_result: str
    evaluation_metric: float

class ProcessedImageCreate(ProcessedImageBase):
    pass

class ProcessedImage(ProcessedImageBase):
    id: int

    class Config:
        orm_mode = True
