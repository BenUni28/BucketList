from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date


class Date(BaseModel):
    name: str

router = APIRouter()


@router.post("/add-item")
async def create_item(date: Date):
    return date