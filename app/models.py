from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class StockPrice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    change_percent: float
    volume: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # אינדיקטורים טכניים
    rsi: Optional[float] = Field(default=None)
    ma20: Optional[float] = Field(default=None)
    ma50: Optional[float] = Field(default=None)

    # סיגנל
    signal: Optional[str] = Field(default=None)

    # רמות מסחר
    entry_low: Optional[float] = Field(default=None)
    entry_high: Optional[float] = Field(default=None)
    stop_loss: Optional[float] = Field(default=None)
    upper_stop: Optional[float] = Field(default=None)
    target: Optional[float] = Field(default=None)


class NewsItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    title: str
    summary: str
    url: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
