import numpy as np
import pandas as pd
import statsmodels.api as sm

def compute_rolling_beta(
    ret: pd.Series,
    market: pd.Series,
    window: int = 12
):
    cov = ret.rolling(window).cov(market)
    var = market.rolling(window).var()
    beta = cov / var
    return beta

# def compute_rolling_beta(
#     stock_returns: pd.DataFrame,
#     market_returns: pd.Series,
#     window: int = 12
# ) -> pd.DataFrame:

#     # Align dates
#     stock_returns, market_returns = stock_returns.align(
#         market_returns, axis=0, join="inner"
#     )

#     market_var = market_returns.rolling(window).var()

#     betas = pd.DataFrame(
#         index=stock_returns.index,
#         columns=stock_returns.columns,
#         dtype=float
#     )

#     # beta=cov(Rm,Ri)/var(Rm)
#     for ticker in stock_returns.columns:
#         cov = (
#             stock_returns[ticker]
#             .rolling(window)
#             .cov(market_returns)
#         )
#         betas[ticker] = cov / market_var

#     return betas
