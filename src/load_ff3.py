import pandas as pd
import zipfile
from pathlib import Path
import requests
import io

FF3_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"
from src.config import FF3_PATH

def download_ff3_data(path=FF3_PATH):
    if not path.exists():
        response = requests.get(FF3_URL)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open(z.namelist()[0]) as f:
                ff3_data = pd.read_csv(f, skiprows=3)
        # Save the data locally
        path.parent.mkdir(parents=True, exist_ok=True)
        ff3_data.to_csv(path, index=False)
        print(f"FF3 data saved to {path}")
    else:
        ff3_data = pd.read_csv(path)

    return ff3_data

if __name__ == "__main__":
    ff3_data = download_ff3_data()
    print(ff3_data.head())