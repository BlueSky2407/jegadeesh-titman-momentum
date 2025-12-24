import numpy as np
import pandas as pd
import statsmodels.api as sm


#CAPM regression using excess returns:
#(Rp - Rf) = alpha + beta * (Rm - Rf) + error

def capm_regression( portfolio_returns: pd.Series,
    market_returns: pd.Series,
    risk_free_rate: pd.Series):
    # Align the indices
    df = pd.concat([portfolio_returns, market_returns, risk_free_rate], axis=1).dropna()
    df.columns = ['rp', 'rm', 'rf']
    Rp = df['rp'] - df['rf']
    Rm = (df['rm'] - df['rf']).rename('Rm')
    X = sm.add_constant(Rm)
    y = Rp
    model = sm.OLS(y,X).fit()
    print(model.params)
    print(model.params.index)
    return {
        'alpha': model.params['const'],
        'beta': model.params['Rm'],
        't_alpha': model.tvalues['const'],
        't_beta': model.tvalues['Rm'],
        'r_squared': model.rsquared
    }