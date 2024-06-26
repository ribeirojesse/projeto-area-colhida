from fastapi import FastAPI
from .database import engine, Base
from .routers import images

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(images.router)
