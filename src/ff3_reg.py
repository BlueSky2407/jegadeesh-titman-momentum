import numpy as np
import pandas as pd
import statsmodels.api as sm

def ff3_reg( portfolio_returns: pd.Series,
    ff_factors: pd.DataFrame):
    # Align the indices
    df = pd.concat([portfolio_returns, ff_factors], axis=1).dropna()
    Rp = df.iloc[:,0] - df['RF']
    X = df[['RM', 'SMB', 'HML']]
    X = sm.add_constant(X)
    y = Rp
    model = sm.OLS(y,X).fit()
    print(model.params)
    print(model.params.index)
    return {
        'alpha': model.params['const'],
        't_alpha': model.tvalues['const'],
        'beta_mkt': model.params['RM'],
        'beta_smb': model.params['SMB'],
        'beta_hml': model.params['HML'],
        'r_squared': model.rsquared
    }