import yfinance as yf
from sqlmodel import Session
from app.database import engine
from app.models import StockPrice
from datetime import datetime, timezone, timedelta

ISRAEL_TZ = timezone(timedelta(hours=3))


# This is your watchlist - edit these symbols anytime
WATCHLIST = [
    "NVDA", "AAPL", "TSLA", "MSFT", "AMD",
    "GOOGL", "META", "AMZN", "PLTR", "COIN",
    "NFLX", "UBER", "INTC", "BABA", "SMCI", "BTC"
]

#
# WATCHLIST = [
#     # Big Tech
#     "NVDA", "AAPL", "MSFT", "GOOGL", "META", "AMZN", "NFLX", "INTC", "AMD", "SMCI",
#     # Semiconductors
#     "TSM", "QCOM", "AVGO", "MU", "AMAT", "LRCX", "KLAC", "MRVL", "ARM", "ON",
#     # EV & Auto
#     "TSLA", "RIVN", "LCID", "F", "GM", "TM", "STLA", "NIO", "LI", "XPEV",
#     # Finance & Crypto
#     "COIN", "MSTR", "JPM", "BAC", "GS", "MS", "V", "MA", "PYPL", "SQ",
#     # Retail & Consumer
#     "AMZN", "WMT", "TGT", "COST", "HD", "NKE", "SBUX", "MCD", "BABA", "JD",
#     # Cloud & Software
#     "CRM", "ORCL", "NOW", "SNOW", "PLTR", "UBER", "LYFT", "SHOP", "DDOG", "NET",
#     # Healthcare & Pharma
#     "JNJ", "PFE", "MRNA", "LLY", "ABBV", "BMY", "UNH", "CVS", "AMGN", "GILD",
#     # Energy & Oil
#     "XOM", "CVX", "OXY", "BP", "SLB", "HAL", "MPC", "VLO", "COP", "EOG",
#     # Space & Defense
#     "LMT", "RTX", "NOC", "BA", "GD", "RKLB", "SPCE", "ASTS", "LUNR", "JOBY",
#     # ETFs & Index
#     "SPY", "QQQ", "ARKK", "SOXL", "TQQQ", "IWM", "DIA", "XLF", "XLE", "UVXY",
#     "BRK.B", "V", "MA", "WMT", "UNH", "HD", "PG", "KO", "DIS", "IBM", "GE",
#     "CAT", "PEP", "CSCO", "TXN", "ADBE"
#
# ]
#

def fetch_prices():
    print(f"[Price Agent] Fetching prices at {datetime.now(ISRAEL_TZ).strftime('%H:%M:%S')}")

    for symbol in WATCHLIST:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info

            price = round(info.last_price, 2)
            prev_close = round(info.previous_close, 2)
            change_percent = round(((price - prev_close) / prev_close) * 100, 2)
            volume = int(info.last_volume)

            stock = StockPrice(
                symbol=symbol,
                price=price,
                change_percent=change_percent,
                volume=volume,
                timestamp=datetime.now(ISRAEL_TZ)
            )

            with Session(engine) as session:
                session.add(stock)
                session.commit()

            print(f"  {symbol}: ${price} ({change_percent:+.2f}%)")

        except Exception as e:
            print(f"  [Error] {symbol}: {e}")