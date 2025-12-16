from sqlalchemy import Column, String, Date, DateTime
from database import Base
from datetime import datetime


class BucketItem(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    what = Column(String, nullable=False)
    where = Column(String, nullable=False)
    when = Column(Date, nullable=True)
    link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
