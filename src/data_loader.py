import pandas as pd
import yfinance as yf
from pathlib import Path

from src.config import START_DATE, END_DATE, DATA_FREQUENCY, MAX_STOCKS, PRICES_PATH
from src.universe import get_universe

def download_data(save_path = PRICES_PATH):
    print("Downloading stock price data...")
    tickers = get_universe(max_stocks=MAX_STOCKS)
    print(f"number of tickers = {len(tickers)}")
    prices = yf.download(
            tickers, 
            start=START_DATE, 
            end=END_DATE, 
            interval=DATA_FREQUENCY,  
            auto_adjust=True)["Close"]
    prices.dropna(how='all', inplace=True)
    print(prices.head())
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    prices.to_csv(save_path)
    print(f"Price data saved to {save_path}")

    return prices

if __name__ == "__main__":
    download_data()