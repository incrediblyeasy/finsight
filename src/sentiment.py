# pipeline is a HuggingFace function that makes using AI models very simple
# Instead of writing complex model code, pipeline wraps everything for us
# You just say "I want sentiment analysis" and it handles the rest
from transformers import pipeline

# torch is PyTorch - the engine that actually runs the math inside the AI model
# We don't use it directly but transformers needs it running in the background
import torch


def load_model():
    # This function downloads and loads the FinBERT model
    # FinBERT is stored on HuggingFace's servers at this address:
    # "ProsusAI/finbert"
    # First time you run this, it downloads ~500MB - takes a few minutes
    # After that it's cached on your computer, runs instantly

    print("Loading FinBERT model... (first time takes 2-3 minutes)")

    # pipeline() creates a ready-to-use AI tool
    # "sentiment-analysis" tells it what task we want
    # model="ProsusAI/finbert" tells it which specific model to use
    # device=-1 means "use CPU" (not GPU) - fine for our project
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert",
        device=-1
    )

    print("Model loaded successfully!")
    return sentiment_pipeline


def analyze_headlines(headlines, sentiment_pipeline):
    # headlines = list of headline dictionaries from fetch_news.py
    # sentiment_pipeline = the loaded AI model

    results = []  # we'll store our results here

    for article in headlines:
        title = article["title"]

        # Feed the headline title into the AI model
        # The model returns a list with one dictionary inside
        # Example output: [{"label": "negative", "score": 0.94}]
        # We take [0] because it always returns a list, we want the first item
        prediction = sentiment_pipeline(title)[0]

        # prediction["label"] = "positive", "negative", or "neutral"
        # prediction["score"] = confidence between 0 and 1
        # 0.94 means the model is 94% confident in its answer

        sentiment = prediction["label"]    # e.g. "negative"
        confidence = round(prediction["score"] * 100, 1)  # convert to percentage

        # Build a result dictionary combining the headline + AI score
        result = {
            "title": title,
            "sentiment": sentiment,
            "confidence": confidence,
            "published_at": article["published_at"],
            "url": article["url"]
        }

        results.append(result)

    return results


def get_overall_signal(results):
    # This function looks at ALL headlines and gives one final signal
    # It counts how many are positive, negative, neutral
    # and returns "BULLISH", "BEARISH", or "NEUTRAL"

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for r in results:
        if r["sentiment"] == "positive":
            positive_count += 1
        elif r["sentiment"] == "negative":
            negative_count += 1
        else:
            neutral_count += 1

    # Simple scoring: whichever has the most wins
    if positive_count > negative_count and positive_count > neutral_count:
        signal = "BULLISH"      # more good news = likely going up
        emoji = "📈"
    elif negative_count > positive_count and negative_count > neutral_count:
        signal = "BEARISH"      # more bad news = likely going down
        emoji = "📉"
    else:
        signal = "NEUTRAL"      # mixed or unclear
        emoji = "➡️"

    return {
        "signal": signal,
        "emoji": emoji,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count
    }


if __name__ == "__main__":
    # We import our fetch_news function from the other file
    # This is how Python files talk to each other
    from fetch_news import get_news

    ticker = "AAPL"
    company_name = "Apple"

    # Step 1: get headlines
    print("Fetching headlines...")
    headlines = get_news(ticker, company_name)

    # Step 2: load the AI model
    model = load_model()

    # Step 3: analyze each headline
    print("\nAnalyzing sentiment of each headline...\n")
    print("-" * 70)

    results = analyze_headlines(headlines, model)

    # Step 4: print each result with color-coded label
    for i, r in enumerate(results, start=1):
        # Pick a symbol based on sentiment so it's easy to read
        if r["sentiment"] == "positive":
            icon = "✅"
        elif r["sentiment"] == "negative":
            icon = "❌"
        else:
            icon = "➖"

        print(f"{i}. {r['title'][:80]}...")   # [:80] limits title to 80 chars
        print(f"   {icon} {r['sentiment'].upper()} — {r['confidence']}% confident")
        print()

    print("-" * 70)

    # Step 5: get and print the overall signal
    signal = get_overall_signal(results)

    print(f"\n{'='*40}")
    print(f"  OVERALL SIGNAL: {signal['emoji']} {signal['signal']}")
    print(f"{'='*40}")
    print(f"  Positive headlines: {signal['positive']}")
    print(f"  Negative headlines: {signal['negative']}")
    print(f"  Neutral  headlines: {signal['neutral']}")
    print(f"{'='*40}\n")