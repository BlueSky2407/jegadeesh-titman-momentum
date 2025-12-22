from pathlib import Path

#Tim period
START_DATE = '2000-01-01'
END_DATE = '2024-01-01'

#Stock universe(cuurent constituents of S&P 500)
MAX_STOCKS = 300 

#Data parameters
DATA_FREQUENCY = "1mo"   # monthly data
USE_ADJUSTED_PRICES = True

DATA_DIR = Path("data")
PRICES_PATH = Path("data/raw/prices.csv")
UNIVERSE_CSV_PATH = Path("data/sp500_companies.csv")