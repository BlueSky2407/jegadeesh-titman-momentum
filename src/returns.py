import pandas as pd
import numpy as np
from pathlib import Path

from src.config import PRICES_PATH, DATA_DIR

def load_prices(path=PRICES_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Price data not found at {path}. Run data_loader.py first.")
    prices = pd.read_csv(path, index_col=0, parse_dates=True)
    return prices

def compute_monthly_returns(prices):
    returns = prices.pct_change(fill_method=None).dropna(how="all")
    return returns

#computer formation period(J months) returns 
def compute_J_returns(returns,J):  

    #remember that we need stocks who have returns from t-1 to t-J, ie if any stock IPOd recently we cannot use it for formation period returns
    formation_returns = (
        (1 + returns)
        .rolling(window=J, min_periods=J)
        .apply(lambda x: np.prod(x) - 1, raw=True)
    )
    return formation_returns

if __name__ == "__main__":
    prices = load_prices()
    returns = compute_monthly_returns(prices)
    print("Monthly return \n")
    print(returns.head())
    processed_dir = DATA_DIR / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    returns.to_csv(processed_dir / "monthly_returns.csv")
    for j in [3, 6, 9, 12]:  # 4 quarters
        J_returns = compute_J_returns(returns,j)
        print(f"\n {j} month returns \n")
        print(J_returns.head())
        save_path = processed_dir / f"formation_J_{j}_returns.csv"
        J_returns.to_csv(save_path) 
