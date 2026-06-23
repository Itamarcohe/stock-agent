import feedparser
from sqlmodel import Session
from app.database import engine
from app.models import NewsItem
from datetime import datetime

# Free RSS feeds - no API key needed
RSS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
    "Seeking Alpha": "https://seekingalpha.com/feed.xml",
}

# Keywords to filter for relevant news
KEYWORDS = ["NVDA", "nvidia", "AAPL", "apple", "TSLA", "tesla", "stock", "market", "trump"]


def fetch_news():
    print(f"[News Agent] Fetching news at {datetime.utcnow().strftime('%H:%M:%S')}")

    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:  # only take 5 latest per source
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                link = entry.get("link", "")

                # only save if relevant to our keywords
                combined = (title + summary).lower()
                if not any(kw.lower() in combined for kw in KEYWORDS):
                    continue

                news = NewsItem(
                    source=source_name,
                    title=title,
                    summary=summary[:500],  # trim long summaries
                    url=link,
                    timestamp=datetime.utcnow()
                )

                with Session(engine) as session:
                    session.add(news)
                    session.commit()

                print(f"  [{source_name}] {title[:60]}...")

        except Exception as e:
            print(f"  [Error] {source_name}: {e}")