from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import json


DATA_FILE = Path("data.json")

router = APIRouter()

dates = []

class Date(BaseModel):
    name: str

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@router.post("/add-item")
async def create_item(date: Date):
    dates = load_data()
    dates.append(date.name)
    save_data(dates)
    return {"message": f"Item '{date.name}' added successfully!", "items": dates}

@router.get("/all-items")
async def get_items():
    return {"items": load_data()}

@router.delete("/delete-item/{name}")
async def delete_item(name: str):
    dates = load_data()
    if name in dates:
        dates.remove(name)
        save_data(dates)
        return {"message": f"Item '{name}' deleted successfully!", "items": dates}
    return {"message": f"Item '{name}' not found.", "items": dates}