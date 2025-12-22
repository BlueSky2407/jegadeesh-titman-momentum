import pandas as pd

from src.config import UNIVERSE_CSV_PATH

def get_universe(max_stocks=None):
    # url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    # tables = pd.read_html(url)
    # sp500 = tables[0]

    if not UNIVERSE_CSV_PATH.exists():
        raise FileNotFoundError(f"Universe CSV not found at {UNIVERSE_CSV_PATH}")
    
    sp500_df = pd.read_csv(UNIVERSE_CSV_PATH)
    tickers = sp500_df['Symbol'].str.replace('.', '-').tolist()

    if max_stocks is not None:
        return tickers[:max_stocks]
