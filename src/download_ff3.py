import pandas as pd
import zipfile
import requests
import io
from pathlib import Path

from src.config import FF3_PATH, DATA_DIR

FF3_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"


def download_ff3_data(path=FF3_PATH):
    if not path.exists():
        response = requests.get(FF3_URL)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open(z.namelist()[0]) as f:
                ff3_data = pd.read_csv(f, skiprows=3)

        path.parent.mkdir(parents=True, exist_ok=True)
        ff3_data.to_csv(path, index=False)
        print(f"FF3 data saved to {path}")
    else:
        print(f"FF3 data already exists at {path}")


def load_ff3(path=FF3_PATH):
    if not path.exists():
        raise FileNotFoundError(
            f"FF3 data not found at {path}. Run download_ff3_data first."
        )

    ff3_data = pd.read_csv(path)

    ff3_data.columns = ['Date', 'RM', 'SMB', 'HML', 'RF']

    # Remove annual/footer rows
    ff3_data['Date'] = ff3_data['Date'].astype(str).str.strip()
    ff3_data = ff3_data[ff3_data['Date'].astype(str).str.len() == 6]

    ff3_data['Date'] = pd.to_datetime(ff3_data['Date'], format='%Y%m')

    for col in ['RM', 'SMB', 'HML', 'RF']:
        ff3_data[col] = pd.to_numeric(ff3_data[col], errors='coerce') / 100

    # Proper time-series index
    ff3_data = ff3_data.set_index('Date').sort_index()

    out_path = DATA_DIR / "portfolio" / "ff3.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ff3_data.to_csv(out_path)

    return ff3_data


if __name__ == "__main__":
    download_ff3_data()
    ff3 = load_ff3()
    print(ff3.head())
