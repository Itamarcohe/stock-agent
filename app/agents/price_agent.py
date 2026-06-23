import yfinance as yf
import pandas as pd
import ta
from sqlmodel import Session, select
from app.database import engine
from app.models import StockPrice
from datetime import datetime, timezone, timedelta

ISRAEL_TZ = timezone(timedelta(hours=3))

# WATCHLIST = [
#     "NVDA", "AAPL", "TSLA", "MSFT", "AMD",
#     "GOOGL", "META", "AMZN", "PLTR", "COIN",
#     "NFLX", "UBER", "INTC", "BABA", "SMCI",
#     "BRK.B", "V", "MA", "WMT", "UNH", "HD", "PG", "KO", "DIS", "IBM",
#     "GE", "CAT", "PEP", "CSCO", "TXN", "ADBE",
#     "TSM", "QCOM", "AVGO", "MU", "AMAT", "MRVL", "ARM",
#     "RIVN", "F", "GM", "NIO",
#     "JPM", "BAC", "GS", "MS", "PYPL", "SQ",
#     "CRM", "ORCL", "NOW", "SNOW", "DDOG", "NET", "SHOP",
#     "JNJ", "PFE", "MRNA", "LLY", "ABBV",
#     "XOM", "CVX", "OXY",
#     "LMT", "BA", "RKLB",
#     "SPY", "QQQ", "ARKK"
# ]
#

WATCHLIST = [
    "NVDA", "AAPL", "TSLA", "MSFT", "AMD"]



def calc_signal(rsi, price, ma20, ma50):
    """החלטה על בסיס RSI וממוצעים נעים"""
    if rsi is None:
        return "מעקב", None, None, None, None

    entry_low = round(price * 0.998, 2)
    entry_high = round(price * 1.002, 2)
    stop = round(price * 0.975, 2)
    upper_stop = round(price * 1.035, 2)
    target = round(price * 1.05, 2)

    # RSI מתחת ל-30 = oversold = קנייה
    # RSI מעל 70 = overbought = מכירה
    # מחיר מעל MA20 וMA50 = מגמה חיובית
    if rsi < 30:
        action = "קנייה חזקה"
    elif rsi < 45 and price > ma20:
        action = "קנייה"
    elif rsi > 70:
        action = "מכירה"
    elif rsi > 60 and price < ma20:
        action = "המתנה"
    else:
        action = "מעקב"

    return action, entry_low, entry_high, stop, upper_stop, target


def fetch_prices():
    print(f"[Price Agent] Fetching prices at {datetime.now(ISRAEL_TZ).strftime('%H:%M:%S')}")

    for symbol in WATCHLIST:
        try:
            ticker = yf.Ticker(symbol)

            # שולפים 60 ימים אחרונים לחישוב אינדיקטורים
            hist = ticker.history(period="60d", interval="1d")

            if hist.empty or len(hist) < 20:
                print(f"  [Skip] {symbol}: not enough data")
                continue

            close = hist["Close"]
            price = round(float(close.iloc[-1]), 2)
            prev_close = round(float(close.iloc[-2]), 2)
            change_percent = round(((price - prev_close) / prev_close) * 100, 2)
            volume = int(hist["Volume"].iloc[-1])

            # חישוב אינדיקטורים
            rsi_series = ta.momentum.RSIIndicator(close, window=14).rsi()
            rsi = round(float(rsi_series.iloc[-1]), 1) if not rsi_series.empty else None

            ma20 = round(float(close.rolling(20).mean().iloc[-1]), 2)
            ma50 = round(float(close.rolling(50).mean().iloc[-1]), 2) if len(close) >= 50 else ma20

            action, entry_low, entry_high, stop, upper_stop, target = calc_signal(rsi, price, ma20, ma50)

            stock = StockPrice(
                symbol=symbol,
                price=price,
                change_percent=change_percent,
                volume=volume,
                rsi=rsi,
                ma20=ma20,
                ma50=ma50,
                signal=action,
                entry_low=entry_low,
                entry_high=entry_high,
                stop_loss=stop,
                upper_stop=upper_stop,
                target=target,
                timestamp=datetime.now(ISRAEL_TZ)
            )

            with Session(engine) as session:
                session.add(stock)
                session.commit()

            print(f"  {symbol}: ${price} ({change_percent:+.2f}%) RSI={rsi} → {action}")

        except Exception as e:
            print(f"  [Error] {symbol}: {e}")