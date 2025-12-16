from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
from models import Base
from routes import add_item

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bucket List API",
    description="API for managing a bucket list of dating ideas.",
    version="1.0.0",
    reload=True
)

app.include_router(add_item.router, prefix="/items")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
