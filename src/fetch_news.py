# "os" is a built-in Python library (no install needed)
# It lets Python talk to your operating system
# We use it here to READ the .env file and get our secret API key
import os

# "requests" lets Python make HTTP requests
# HTTP is the language browsers use to fetch websites
# We use it to call the NewsAPI like a browser would
import requests

# "dotenv" reads our .env file and loads the keys into memory
# So our code can access them without us hardcoding the key in the file
from dotenv import load_dotenv

# This line actually reads the .env file
# It looks for .env in the parent folder (one level up from src/)
load_dotenv("../.env")


def get_news(ticker, company_name):
    # ticker = "AAPL", company_name = "Apple"
    # We need the company name because news articles say "Apple" not "AAPL"

    # os.getenv() reads a value from the .env file
    # This is how we safely use secret keys without exposing them
    api_key = os.getenv("NEWS_API_KEY")

    # This is the URL we are calling - like typing it in a browser
    # It's called an "API endpoint" - a URL that returns data instead of a webpage
    # We are building the URL with our search term and key
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company_name}+stock+OR+{ticker}+earnings+OR+{company_name}+market&"           # search query
        f"language=en&"                # only english articles
        f"sortBy=publishedAt&"         # newest first
        f"pageSize=10&"                # only get 10 articles
        f"apiKey={api_key}"            # our secret key
    )

    # requests.get() sends a GET request to that URL
    # Like your browser visiting a webpage, but the response is JSON data
    response = requests.get(url)

    # response.json() converts the raw response into a Python dictionary
    # A dictionary is like a real dictionary - you look up a key, get a value
    # Example: data["status"] gives us "ok" or "error"
    data = response.json()

    # Check if the API call was successful
    if data["status"] != "ok":
        print("Error fetching news:", data.get("message", "Unknown error"))
        return []

    # data["articles"] is a list of article dictionaries
    # Each article has keys like "title", "description", "url", "publishedAt"
    articles = data["articles"]

    # We only want to keep 3 things from each article
    # We use a "list comprehension" - a clean way to loop and build a list
    # For each article in articles, create a small dictionary with just what we need
    headlines = [
        {
            "title": article["title"],
            "description": article["description"],
            "published_at": article["publishedAt"],
            "url": article["url"]
        }
        for article in articles
        if article["title"] is not None  # skip articles with no title
    ]

    return headlines


if __name__ == "__main__":

    ticker = "AAPL"
    company_name = "Apple"

    print(f"Fetching news for {company_name}...")
    print("-" * 60)

    headlines = get_news(ticker, company_name)

    # Loop through each headline and print it
    # "enumerate" gives us both the index (i) and the item (article)
    # So we can print "1.", "2.", "3." etc.
    for i, article in enumerate(headlines, start=1):
        print(f"{i}. {article['title']}")
        print(f"   Published: {article['published_at'][:10]}")  # [:10] cuts the time, keeps only date
        print(f"   URL: {article['url']}")
        print()

    print(f"Total headlines fetched: {len(headlines)}")