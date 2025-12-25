import numpy as np
import pandas as pd
import statsmodels.api as sm
import yfinance as yf

from src.config import START_DATE, END_DATE, DATA_FREQUENCY, RF_CSV_PATH, DATA_DIR

def get_market_returns(START_DATE, END_DATE, DATA_FREQUENCY):
    market_data = yf.download(
        "^GSPC", 
        start=START_DATE, 
        end=END_DATE, 
        interval=DATA_FREQUENCY,
        auto_adjust=True)["Close"]
    market_returns = market_data.pct_change().dropna()
    market_returns = market_returns.rename(columns={"^GSPC":"Market_Returns"})
    print(market_returns.head())
    return market_returns

def get_rf(path=RF_CSV_PATH):
    rf = pd.read_csv(path, parse_dates=["observation_date"])
    rf = rf.rename(columns={"observation_date": "Date", "TB4WK": "Rf_Rate"})
    rf = rf.set_index("Date")
    #since the rf rate is in annual percentage, we convert it to monthly decimal
    rf["Rf_Rate"] = rf["Rf_Rate"] / 100 / 12
    print(rf.head())
    return rf

if __name__ == "__main__":
    market_returns = get_market_returns(START_DATE, END_DATE, DATA_FREQUENCY)
    rf = get_rf()
    path1 = DATA_DIR / "portfolio" / f"market_returns.csv"
    path1.parent.mkdir(parents=True, exist_ok=True)
    path2 = DATA_DIR / "portfolio" / f"rf_rate.csv"
    path2.parent.mkdir(parents=True, exist_ok=True)
    market_returns.to_csv(path1)
    rf.to_csv(path2)