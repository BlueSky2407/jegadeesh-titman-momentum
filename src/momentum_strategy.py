#important points
# formation period : t-J...t-1
# formation period returns indexed at t-1
# portfolio construction at beginning of t
# holding period : t...t+K-1(case 1)
# holding period : t+1...t+K(case 2)

import pandas as pd
import numpy as np
from pathlib import Path

from src.config import DATA_DIR

def get_J_returns(J):
    path = DATA_DIR /"processed"/ f"formation_J_{J}_returns.csv"
    if not path.exists():
        print(f"cannot find formation {J} returns. Run returns.py first")
    returns = pd.read_csv(path, index_col=0, parse_dates = True)
    return returns

def rank_stocks(returns, n_deciles=10):
    def decile_rank(row):
        valid_row = row.dropna()
        if(len(valid_row)<n_deciles):
            #send row with all NaNs if not enough stocks to form deciles
            return pd.Series(index=row.index, dtype=float)
        
        #pd.qcut: Sorts values and splits them into quantiles with equal counts
        ranks = pd.qcut(valid_row, q=n_deciles, labels=False) + 1  #deciles 1 to 10
        #reyurn a series with same index as original row but values as the decile ranks
        out = pd.Series(index=row.index, dtype=float)
        out[valid_row.index] = ranks
        return out
    deciles = returns.apply(decile_rank, axis =1) #since axis 1 means compuyte the function across all columns for each row
    return deciles

def get_winner_loser_masks(deciles):
    #we ranked them in asceding order of returns 
    winners = deciles == 10
    losers = deciles == 1
    
    return winners, losers

if __name__ == "__main__":
    J = 6
    J_returns = get_J_returns(J)
    deciles = rank_stocks(J_returns)
    winners, losers = get_winner_loser_masks(deciles)
    print(J_returns[0:10][0:20])
    print(deciles[0:10][0:20])
    print(winners[0:10][0:20])
    print(losers[0:10][0:20])

