# Stock Agent — AI Market Assistant

Real-time stock analysis system with a Hebrew RTL dashboard, powered by Python and FastAPI.

## What It Does

- Fetches real-time stock prices from Yahoo Finance
- Calculates RSI, MA20, MA50 and generates buy/sell signals
- Analyzes company quality (profitability, growth, debt, cash flow)
- Displays relevant financial news from RSS feeds
- Hebrew RTL dashboard with auto-refresh every 30 seconds

---

## Installation — Step by Step

### 1. Install Python
Download from: https://www.python.org/downloads/

Important: choose version 3.10 to 3.13 — do NOT use 3.14

During installation, check "Add Python to PATH"

### 2. Install Node.js
Download from: https://nodejs.org

Choose the LTS version and run the installer.

### 3. Install PyCharm Community
Download from: https://www.jetbrains.com/pycharm/download

Choose Community Edition (free) and run the installer.

### 4. Install Git
Download from: https://git-scm.com/downloads

Run the installer with default settings.

---

## Clone the Project

Open a terminal and run:

    git clone https://github.com/Itamarcohe/stock-agent.git
    cd stock-agent

---

## Set Up the Environment

    python -m venv .venv
    .venv\Scripts\activate
    pip install fastapi uvicorn yfinance feedparser sqlmodel aiohttp apscheduler pandas ta

---

## Run the Server

    python run.py

You will see stocks loading in the terminal with RSI and signals.

---

## Open the Dashboard

After the server starts, open in your browser:

- Hebrew dashboard: open dashboard_he.html directly in Chrome
- API explorer: http://localhost:8000/docs
- Prices: http://localhost:8000/prices
- News: http://localhost:8000/news
- Quality analysis: http://localhost:8000/quality/NVDA

---

## Project Structure

    stock-agent/
    ├── app/
    │   ├── agents/
    │   │   ├── price_agent.py       fetches prices and calculates RSI
    │   │   ├── news_agent.py        fetches news from RSS feeds
    │   │   └── quality_agent.py     analyzes company quality
    │   ├── main.py                  FastAPI server and endpoints
    │   ├── models.py                database models
    │   └── database.py              SQLite setup
    ├── dashboard_he.html            Hebrew RTL dashboard
    ├── dashboard.html               English dashboard
    └── run.py                       start the server

---

## Where We Left Off

Next agent to build: Dip Opportunity Agent
File: app/agents/dip_agent.py

This agent checks whether a sharp price drop is a buying opportunity or a danger signal, based on:
- How far the stock dropped from its 60-day high
- RSI level
- Price vs MA20
- Trading volume ratio

After that: Valuation Agent, Market Regime Agent, Long-Term Entry Agent, and more.

---

## Requirements

- Python 3.10 to 3.13
- Node.js LTS
- Internet connection for Yahoo Finance data
- Windows 10 or 11

---

Disclaimer: This project is for educational purposes only and does not constitute investment advice.