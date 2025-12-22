import pandas as pd
import numpy as np
from pathlib import Path

from src.config import DATA_DIR
from src.returns import load_prices, compute_monthly_returns
from src.momentum_strategy import get_winner_loser_masks, rank_stocks, get_J_returns

def compute_portfolio_returns(J, K, skip=0):
    #get all data
    prices = load_prices()
    monthly_returns = compute_monthly_returns(prices)
    formation_returns = get_J_returns(J)
    deciles = rank_stocks(formation_returns)
    winners, losers = get_winner_loser_masks(deciles)

    # if(skip==1):
    #     winners = winners.shift(1)
    #     losers  = losers.shift(1)

    monthly_returns = monthly_returns.loc[winners.index]
    strategy_returns = []

    # “In each month t, 
    # the strategy buys the winner portfolio and sells the loser portfolio, 
    # holding this position for K months.”
    for t in range(len(monthly_returns)):
        row_returns = monthly_returns.iloc[t]
        pnl = []

        #OVERLAPPING PORTFOLIO we hold k portfolios every month
        for k in range(K):
            #formation_idx = t - k 
            eff_formation_idx = t-k-skip
            #if skip is 1 starts earing return at t+1 for portfolio formed at t

            if eff_formation_idx<0: continue

            # winners_mask = winners.iloc[eff_formation_idx].fillna(False)
            # losers_mask = losers.iloc[eff_formation_idx].fillna(False)
            winners_mask = winners.iloc[eff_formation_idx]
            losers_mask = losers.iloc[eff_formation_idx]
            winners_returns = row_returns[winners_mask].mean()
            losers_returns = row_returns[losers_mask].mean()
            if not np.isnan(winners_returns) and not np.isnan(losers_returns):
                returns = winners_returns-losers_returns
                pnl.append(returns)

        if(len(pnl)>0):
            strategy_returns.append(np.mean(pnl))
        else:
            strategy_returns.append(np.nan)

    returns = pd.Series(strategy_returns, 
                        index = monthly_returns.index,
                        name = f"WML_J{J}_K{K}_skip{skip}")
        
    return returns
    
if __name__=="__main__":
    for J in [3,6,9,12]:
        for K in [3,6,9,12]:
            for skip in [0,1]:
                returns = compute_portfolio_returns(J, K, skip)

                start = J + K + skip
                trimmed = returns.iloc[start:].dropna()

                mean_ret = trimmed.mean()

                print(f"J={J} K={K} skip={skip} "f"mean={mean_ret:.4f}")
                #returns_skip0.to_csv(DATA_DIR / "portfolio" / f"WML_J{J}_K{K}_skip0.csv")
                #returns_skip1.to_csv(DATA_DIR / "portfolio" / f"WML_J{J}_K{K}_skip1.csv")
