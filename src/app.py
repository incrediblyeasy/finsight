# streamlit is our web framework - turns Python into a webpage
import streamlit as st

# plotly makes interactive charts - user can hover, zoom etc
import plotly.graph_objects as go

# we import our own functions from the other files we already built
import sys
import os

# This line tells Python to look for files in the src folder
# Because app.py, fetch_price.py etc are all in the same src folder
sys.path.append(os.path.dirname(__file__))

from fetch_price import get_stock_price, get_latest_price
from fetch_news import get_news
from sentiment import load_model, analyze_headlines, get_overall_signal


# -------------------------------------------------------
# PAGE CONFIGURATION
# This must be the very first streamlit command in the file
# -------------------------------------------------------
st.set_page_config(
    page_title="FinSight - AI Stock Analyzer",
    page_icon="📈",
    layout="wide"   # uses full screen width
)


# -------------------------------------------------------
# CUSTOM STYLING
# st.markdown() lets us inject CSS to style the page
# unsafe_allow_html=True means "yes I know I'm writing HTML, allow it"
# -------------------------------------------------------
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a2e;
        }
        .subtitle {
            font-size: 1rem;
            color: #666;
            margin-top: -15px;
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #e0e0e0;
        }
        .signal-bullish {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 10px 24px;
            border-radius: 20px;
            font-size: 1.3rem;
            font-weight: 700;
            display: inline-block;
        }
        .signal-bearish {
            background: #ffebee;
            color: #c62828;
            padding: 10px 24px;
            border-radius: 20px;
            font-size: 1.3rem;
            font-weight: 700;
            display: inline-block;
        }
        .signal-neutral {
            background: #fff8e1;
            color: #f57f17;
            padding: 10px 24px;
            border-radius: 20px;
            font-size: 1.3rem;
            font-weight: 700;
            display: inline-block;
        }
        .headline-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 8px 0;
            border-left: 4px solid #ccc;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .headline-positive { border-left-color: #4caf50; }
        .headline-negative { border-left-color: #f44336; }
        .headline-neutral  { border-left-color: #ff9800; }
    </style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown('<p class="main-title">📈 FinSight</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Stock Sentiment Analyzer</p>', unsafe_allow_html=True)
st.divider()  # draws a horizontal line


# -------------------------------------------------------
# SIDEBAR
# Everything inside "with st.sidebar" appears in the left panel
# This is where the user types the stock ticker
# -------------------------------------------------------
with st.sidebar:
    st.header("🔍 Search")

    # Text input box - user types a ticker here
    # value="AAPL" is the default value shown in the box
    ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper()

    # Dictionary mapping tickers to company names
    # We need the company name for the news search
    company_map = {
        "AAPL": "Apple",
        "TSLA": "Tesla",
        "GOOGL": "Google",
        "MSFT": "Microsoft",
        "AMZN": "Amazon",
        "NVDA": "NVIDIA",
        "META": "Meta",
        "NFLX": "Netflix"
    }

    # .get() looks up the ticker in our dictionary
    # If not found, it uses the ticker itself as the company name
    company_name = company_map.get(ticker, ticker)

    # Big green button - nothing runs until user clicks this
    analyze_button = st.button("🚀 Analyze", use_container_width=True)

    st.divider()
    st.caption("Powered by FinBERT + NewsAPI + yfinance")


# -------------------------------------------------------
# MAIN LOGIC
# Everything below only runs when the button is clicked
# "if analyze_button" means "if the button was pressed"
# -------------------------------------------------------
if analyze_button:

    # st.spinner shows a loading animation while code runs inside it
    # "with" is a Python context manager - code inside runs together
    with st.spinner(f"Fetching data for {ticker}..."):

        # --- LOAD MODEL ---
        # st.cache_resource is very important!
        # It means: "load the model once, save it in memory"
        # Without this, the 438MB model would re-download every time
        # the user clicks Analyze. With this, it loads once and stays.
        @st.cache_resource
        def get_model():
            return load_model()

        model = get_model()

        # --- FETCH DATA ---
        # Call our functions from the other files
        price_data = get_stock_price(ticker)
        latest_price = get_latest_price(ticker)
        headlines = get_news(ticker, company_name)
        sentiment_results = analyze_headlines(headlines, model)
        signal = get_overall_signal(sentiment_results)


    # -------------------------------------------------------
    # TOP METRICS ROW
    # st.columns(3) creates 3 equal columns side by side
    # col1, col2, col3 are the three columns
    # -------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # st.metric shows a big number with a label
        st.metric(label="💰 Latest Price", value=f"${latest_price}")

    with col2:
        st.metric(label="📰 Headlines Analyzed", value=len(sentiment_results))

    with col3:
        st.metric(label="✅ Positive", value=signal["positive"])

    with col4:
        st.metric(label="❌ Negative", value=signal["negative"])

    st.divider()


    # -------------------------------------------------------
    # OVERALL SIGNAL BADGE
    # -------------------------------------------------------
    st.subheader("🎯 Overall Market Signal")

    # Pick the CSS class based on the signal
    if signal["signal"] == "BULLISH":
        badge_class = "signal-bullish"
        signal_text = "📈 BULLISH — More positive news than negative"
    elif signal["signal"] == "BEARISH":
        badge_class = "signal-bearish"
        signal_text = "📉 BEARISH — More negative news than positive"
    else:
        badge_class = "signal-neutral"
        signal_text = "➡️ NEUTRAL — Mixed or unclear sentiment"

    st.markdown(f'<div class="{badge_class}">{signal_text}</div>',
                unsafe_allow_html=True)

    st.divider()


    # -------------------------------------------------------
    # TWO COLUMNS: CHART LEFT, HEADLINES RIGHT
    # st.columns([6,4]) means left column is 60% wide, right is 40%
    # -------------------------------------------------------
    chart_col, news_col = st.columns([6, 4])


    # --- LEFT: PRICE CHART ---
    with chart_col:
        st.subheader(f"📊 {ticker} — Last 30 Days")

        # Create a candlestick chart using plotly
        # Candlestick charts are the standard in finance
        # Each "candle" shows Open, High, Low, Close for one day
        fig = go.Figure(data=[go.Candlestick(
            x=price_data.index,        # dates on x axis
            open=price_data["Open"],   # opening price
            high=price_data["High"],   # highest price of day
            low=price_data["Low"],     # lowest price of day
            close=price_data["Close"], # closing price
            increasing_line_color="green",   # green candle = price went up
            decreasing_line_color="red"      # red candle = price went down
        )])

        # Style the chart
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_rangeslider_visible=False,  # hide the range slider at bottom
            margin=dict(l=0, r=0, t=10, b=0)
        )

        # st.plotly_chart displays the chart in the webpage
        # use_container_width=True means stretch to fill the column
        st.plotly_chart(fig, use_container_width=True)


    # --- RIGHT: HEADLINES WITH SENTIMENT ---
    with news_col:
        st.subheader("📰 News Sentiment")

        for r in sentiment_results:
            # Pick color and icon based on sentiment
            if r["sentiment"] == "positive":
                css_class = "headline-positive"
                icon = "✅"
            elif r["sentiment"] == "negative":
                css_class = "headline-negative"
                icon = "❌"
            else:
                css_class = "headline-neutral"
                icon = "➖"

            # Build an HTML card for each headline
            # We use f-strings to insert the actual data
            st.markdown(f"""
                <div class="headline-card {css_class}">
                    <div style="font-size:0.85rem; font-weight:600; margin-bottom:5px;">
                        {icon} {r['sentiment'].upper()} — {r['confidence']}%
                    </div>
                    <div style="font-size:0.8rem; color:#333; line-height:1.4;">
                        {r['title'][:100]}...
                    </div>
                    <div style="font-size:0.7rem; color:#999; margin-top:5px;">
                        {r['published_at'][:10]}
                    </div>
                </div>
            """, unsafe_allow_html=True)


    st.divider()
    st.caption("⚠️ This is not financial advice. For educational purposes only.")


# -------------------------------------------------------
# SHOWN BEFORE BUTTON IS CLICKED
# -------------------------------------------------------
else:
    st.info("👈 Enter a stock ticker in the sidebar and click Analyze to get started!")
    
    # Show example tickers as quick-start chips
    st.markdown("**Try these tickers:** `AAPL` `TSLA` `GOOGL` `NVDA` `MSFT`")
