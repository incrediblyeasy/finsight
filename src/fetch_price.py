# We are importing a library called yfinance
# A library is a collection of pre-written code that someone else wrote
# So we don't have to write everything from scratch
import yfinance as yf

# We are importing pandas - this helps us work with tables of data
# We give it a short nickname "pd" so we don't have to type "pandas" every time
import pandas as pd


def get_stock_price(ticker):
    # A "function" is a reusable block of code
    # "ticker" is the input - like AAPL for Apple, TSLA for Tesla

    # yf.Ticker() creates an object that represents one company
    # Think of it like creating a "profile" for that stock
    stock = yf.Ticker(ticker)

    # .history() fetches the price data from Yahoo Finance
    # period="30d" means "give me the last 30 days"
    # This goes to the internet and downloads real data
    data = stock.history(period="30d")

    # "data" is now a DataFrame
    # A DataFrame is like an Excel sheet inside Python - rows and columns
    # Each row = one day, columns = Open, High, Low, Close, Volume

    # We only want these 4 columns, so we select them
    data = data[["Open", "High", "Low", "Close"]]

    # Round every number to 2 decimal places (like money)
    data = data.round(2)

    return data  # send the result back to whoever called this function


def get_latest_price(ticker):
    # This function just gets the single latest closing price
    stock = yf.Ticker(ticker)
    data = stock.history(period="2d")  # get last 2 days

    # .iloc[-1] means "give me the last row"
    # ["Close"] means the closing price column
    latest_price = data["Close"].iloc[-1]

    return round(latest_price, 2)


# This line means: only run the code below if we run THIS file directly
# If another file imports this file, the code below won't run
# This is a standard Python pattern you'll see everywhere
if __name__ == "__main__":

    ticker = "AAPL"  # Apple stock

    print(f"Fetching data for {ticker}...")
    print("-" * 40)  # prints a line of dashes, just for looks

    # Call our function and store the result
    price_data = get_stock_price(ticker)

    # Print the full table
    print(price_data)

    print("-" * 40)

    # Call the second function
    latest = get_latest_price(ticker)
    print(f"Latest closing price of {ticker}: ${latest}")