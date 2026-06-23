import yfinance as yf
from datetime import datetime, timezone, timedelta

ISRAEL_TZ = timezone(timedelta(hours=3))


def analyze_quality(symbol: str) -> dict:
    print(f"[Quality Agent] Analyzing {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        score = 0
        reasons = []
        warnings = []

        # 1. רווחיות
        pe = info.get("trailingPE")
        profit_margin = info.get("profitMargins")
        if profit_margin and profit_margin > 0.1:
            score += 2
            reasons.append(f"מרווח רווח גבוה: {round(profit_margin * 100, 1)}%")
        elif profit_margin and profit_margin > 0:
            score += 1
            reasons.append(f"מרווח רווח חיובי: {round(profit_margin * 100, 1)}%")
        else:
            warnings.append("החברה לא רווחית כרגע")

        # 2. צמיחת הכנסות
        revenue_growth = info.get("revenueGrowth")
        if revenue_growth and revenue_growth > 0.15:
            score += 2
            reasons.append(f"צמיחת הכנסות חזקה: {round(revenue_growth * 100, 1)}%")
        elif revenue_growth and revenue_growth > 0:
            score += 1
            reasons.append(f"צמיחת הכנסות חיובית: {round(revenue_growth * 100, 1)}%")
        else:
            warnings.append("אין צמיחה בהכנסות")

        # 3. חוב
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity is not None:
            if debt_to_equity < 50:
                score += 2
                reasons.append(f"חוב נמוך: {round(debt_to_equity, 1)}")
            elif debt_to_equity < 150:
                score += 1
                reasons.append(f"חוב סביר: {round(debt_to_equity, 1)}")
            else:
                warnings.append(f"חוב גבוה: {round(debt_to_equity, 1)}")

        # 4. תזרים מזומנים
        fcf = info.get("freeCashflow")
        if fcf and fcf > 0:
            score += 2
            reasons.append(f"תזרים מזומנים חיובי: ${round(fcf / 1e9, 1)}B")
        else:
            warnings.append("תזרים מזומנים שלילי")

        # 5. שווי שוק — העדפה לחברות גדולות ויציבות
        market_cap = info.get("marketCap")
        if market_cap and market_cap > 100e9:
            score += 2
            reasons.append(f"חברה גדולה ויציבה: ${round(market_cap / 1e9, 0)}B")
        elif market_cap and market_cap > 10e9:
            score += 1
            reasons.append(f"חברה בינונית: ${round(market_cap / 1e9, 0)}B")
        else:
            warnings.append("חברה קטנה — סיכון גבוה יותר")

        # 6. מכפיל רווח סביר
        if pe and 0 < pe < 25:
            score += 2
            reasons.append(f"מכפיל רווח אטרקטיבי: {round(pe, 1)}")
        elif pe and pe < 40:
            score += 1
            reasons.append(f"מכפיל רווח סביר: {round(pe, 1)}")
        elif pe and pe > 40:
            warnings.append(f"מכפיל רווח גבוה: {round(pe, 1)}")

        # 7. ROE — תשואה על ההון
        roe = info.get("returnOnEquity")
        if roe and roe > 0.15:
            score += 2
            reasons.append(f"תשואה על ההון גבוהה: {round(roe * 100, 1)}%")
        elif roe and roe > 0:
            score += 1
        else:
            warnings.append("תשואה על ההון נמוכה")

        # ציון סופי
        max_score = 14
        pct = round((score / max_score) * 100)

        if pct >= 70:
            quality = "גבוהה"
        elif pct >= 45:
            quality = "בינונית"
        else:
            quality = "נמוכה"

        return {
            "symbol": symbol,
            "quality": quality,
            "score": score,
            "max_score": max_score,
            "percent": pct,
            "reasons": reasons,
            "warnings": warnings,
            "timestamp": datetime.now(ISRAEL_TZ).isoformat()
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "quality": "שגיאה",
            "score": 0,
            "max_score": 14,
            "percent": 0,
            "reasons": [],
            "warnings": [f"שגיאה: {str(e)}"],
            "timestamp": datetime.now(ISRAEL_TZ).isoformat()
        }