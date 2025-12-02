from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import json
from uuid import uuid4
from datetime import date, datetime

DATA_FILE = Path("data.json")

class EntryIn(BaseModel):
    what: Optional[str] = ""
    where: Optional[str] = ""
    when: Optional[date] = None
    link: Optional[str] = ""

router = APIRouter()

def load_data() -> List[dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data: List[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def sort_items(items: List[dict]) -> List[dict]:
    def key_fn(it):
        d = it.get("when")
        if not d:
            return datetime.max
        try:
            return datetime.fromisoformat(d)
        except:
            return datetime.max
    return sorted(items, key=key_fn)

@router.post("/add-item")
async def create_item(entry: EntryIn):
    items = load_data()
    item = {
        "id": str(uuid4()),
        "what": entry.what or "",
        "where": entry.where or "",
        "when": entry.when.isoformat() if entry.when else None,
        "link": entry.link or "",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    items.append(item)
    save_data(items)
    return {"message": "Item added", "items": sort_items(items)}

@router.get("/all-items")
async def get_items():
    items = load_data()
    return {"items": sort_items(items)}

@router.delete("/delete-item/{item_id}")
async def delete_item(item_id: str):
    items = load_data()
    new = [it for it in items if it.get("id") != item_id]
    if len(new) == len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    save_data(new)
    return {"message": "Item deleted", "items": sort_items(new)}
