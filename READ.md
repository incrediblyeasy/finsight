# 📈 FinSight — AI Stock Sentiment Analyzer

An AI-powered web app that analyzes stock market sentiment from real-time news headlines using FinBERT, a finance-specific transformer model.

## 🚀 Live Demo
> Type any stock ticker → get AI sentiment analysis + price chart instantly

## 🛠️ Tech Stack
- **FinBERT** (HuggingFace) — Finance-specific NLP model for sentiment scoring
- **LangChain / Transformers** — AI model pipeline
- **yfinance** — Real-time stock price data
- **NewsAPI** — Live financial news headlines
- **Streamlit** — Web dashboard
- **Plotly** — Interactive candlestick charts
- **Python / Pandas** — Data processing

## 📊 Features
- Enter any stock ticker (AAPL, TSLA, NVDA etc.)
- Fetches last 10 real news headlines
- AI scores each headline: Positive / Negative / Neutral with confidence %
- Overall BULLISH / BEARISH / NEUTRAL signal
- 30-day candlestick price chart

## ⚙️ How to Run Locally

1. Clone the repo
```bash
   git clone https://github.com/YOUR_USERNAME/finsight.git
   cd finsight
```

2. Create virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Add your API key — create a `.env` file: