from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routes import add_item

app = FastAPI()

app.include_router(add_item.router, prefix="/items")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse(Path("static/index.html"))
