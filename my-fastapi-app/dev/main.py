from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routes import add_item

app = FastAPI()

app.include_router(add_item.router, prefix="/items")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
