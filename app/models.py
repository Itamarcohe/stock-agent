from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class StockPrice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    change_percent: float
    volume: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class NewsItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    title: str
    summary: str
    url: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)