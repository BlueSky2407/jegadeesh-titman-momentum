import numpy as np
import pandas as pd

def cumulative_returns(returns: pd.Series) -> pd.Series:
    cumulative = (1 + returns).cumprod()
    return cumulative

def drawdown_series(cum_ret: pd.Series) -> pd.Series:
    peak = cum_ret.cummax()
    drawdown = (cum_ret - peak) / peak
    return drawdown

def max_drawdown(returns: pd.Series) -> float:
    cum_ret = cumulative_returns(returns)
    drawdown = drawdown_series(cum_ret)
    max_dd = drawdown.min()
    return max_dd

def annualized_volatility(returns: pd.Series) -> float:
    vol = returns.std() * np.sqrt(12)  #Annualized volatility
    return vol

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess_returns = returns - risk_free_rate
    mean_excess_return = excess_returns.mean()
    std_excess_return = annualized_volatility(excess_returns)  #Annualized standard deviation
    if std_excess_return == 0:
        return np.nan
    sharpe = mean_excess_return / std_excess_return
    return sharpe

def skewness(returns: pd.Series) -> float:
    return returns.skew()

def rolling_volatility(returns: pd.Series, window: int=12) -> pd.Series:
    return returns.rolling(window=window).std() * np.sqrt(12)  # Annualized rolling realized volatility


def volatility_scaled_returns(
    returns: pd.Series,
    target_vol: float = 0.1,
    window: int = 12,
    periods_per_year: int = 12,
    max_leverage: float | None = 3.0
) -> pd.Series:

    vol = rolling_volatility(returns,window=window)

    scaling_factor = target_vol / vol

    if max_leverage is not None:
        scaling_factor = scaling_factor.clip(upper=max_leverage)

    scaled_returns = scaling_factor.shift(1) * returns
    return scaled_returns.dropna()

