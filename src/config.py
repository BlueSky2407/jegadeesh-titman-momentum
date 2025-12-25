from pathlib import Path

#Tim period
START_DATE = '2000-01-01'
END_DATE = '2024-01-01'

#Stock universe(cuurent constituents of S&P 500)
MAX_STOCKS = 300 

#Data parameters
DATA_FREQUENCY = "1mo"   # monthly data
USE_ADJUSTED_PRICES = True

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PRICES_PATH = DATA_DIR / "raw" / "prices.csv"
UNIVERSE_CSV_PATH = DATA_DIR / "sp500_companies.csv"
RF_CSV_PATH = DATA_DIR / "TB4WK.csv"
FF3_PATH = DATA_DIR / "raw" / "ff3.csv"