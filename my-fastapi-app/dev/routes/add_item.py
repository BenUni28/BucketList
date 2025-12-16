from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from database import SessionLocal
from models import BucketItem

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EntryIn(BaseModel):
    what: Optional[str] = None
    where: Optional[str] = None
    when: Optional[datetime] = None
    link: Optional[str] = None


@router.post("/add-item")
async def create_item(entry: EntryIn, db: Session = Depends(get_db)):
    item = BucketItem(
        id=str(uuid4()),
        what=entry.what or "",
        where=entry.where or "",
        when=entry.when,
        link=entry.link or "",
        created_at=datetime.utcnow()
    )
    
    db.add(item)
    db.commit()

    items = db.query(BucketItem).order_by(
        BucketItem.when.is_(None),
        BucketItem.when
    ).all()

    return {"message": "Item added", "items": items}

@router.get("/get-item/{item_id}")
async def get_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(BucketItem).filter(BucketItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/all-items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(BucketItem).order_by(
        BucketItem.when.is_(None),
        BucketItem.when
    ).all()
    return {"items": items}

@router.delete("/delete-item/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(BucketItem).filter(BucketItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    items = db.query(BucketItem).order_by(
        BucketItem.when.is_(None),
        BucketItem.when
    ).all()

    return {"message": "Item deleted", "items": items}

@router.put("/update-item/{item_id}")
def update_item(item_id: str, entry: EntryIn, db: Session = Depends(get_db)):
    item = db.query(BucketItem).filter(BucketItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.what = entry.what or ""
    item.where = entry.where or ""
    item.when = entry.when
    item.link = entry.link or ""

    db.commit()

    items = db.query(BucketItem).order_by(
        BucketItem.when.is_(None),
        BucketItem.when
    ).all()

    return {"message": "Item updated", "items": items}