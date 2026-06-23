from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import create_db
from app.agents.price_agent import fetch_prices
from app.agents.news_agent import fetch_news
from app.models import StockPrice, NewsItem
from sqlmodel import Session, select
from app.database import engine

app = FastAPI(title="Stock Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()


@app.on_event("startup")
def startup():
    create_db()

    # fetch immediately on startup
    fetch_prices()
    fetch_news()

    # then schedule to run every 5 minutes
    scheduler.add_job(fetch_prices, "interval", minutes=5)
    scheduler.add_job(fetch_news, "interval", minutes=10)
    scheduler.start()
    print("[Server] Scheduler started")


@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()


@app.get("/prices")
def get_prices():
    with Session(engine) as session:
        prices = session.exec(
            select(StockPrice)
            .order_by(StockPrice.timestamp.desc())
            .limit(50)
        ).all()
    return prices


@app.get("/prices/{symbol}")
def get_price_by_symbol(symbol: str):
    with Session(engine) as session:
        prices = session.exec(
            select(StockPrice)
            .where(StockPrice.symbol == symbol.upper())
            .order_by(StockPrice.timestamp.desc())
            .limit(20)
        ).all()
    return prices


@app.get("/news")
def get_news():
    with Session(engine) as session:
        news = session.exec(
            select(NewsItem)
            .order_by(NewsItem.timestamp.desc())
            .limit(50)
        ).all()
    return news


@app.get("/watchlist")
def get_watchlist():
    from app.agents.price_agent import WATCHLIST
    return {"symbols": WATCHLIST}