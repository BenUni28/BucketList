from fastapi import FastAPI
from routes import add_item

app = FastAPI()

app.include_router(add_item.router, prefix="/items")