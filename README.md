# Momentum Investing with Risk Management

This project studies **momentum investing as a systematic trading strategy**, inspired by *Jegadeesh and Titman (1993)* which documents short- to medium-term continuation in stock returns. 

---

## Strategy Overview

The momentum strategy is constructed as follows:

- **J (Formation Period)**:
Stocks are ranked based on their cumulative returns over the past J months.

- **K (Holding Period)**:
Portfolios formed based on the ranking are held for K months.

At each formation date, stocks are sorted into deciles based on past J-month returns. A **winner portfolio** is formed from the top decile, and a **loser portfolio**o from the bottom decile. The momentum strategy goes l**long winners and short losers**.

Portfolios are held with overlapping holding periods, meaning that at any point in time, multiple portfolios formed in previous months are simultaneously active.

Momentum returns are evaluated across multiple J–K combinations.  
For deeper risk analysis and portfolio construction, the benchmark **J = 6, K = 6** strategy is used, as it is widely studied in both the literature and practice.

---

## Data

- **Stock prices & market returns**: Yahoo Finance  
- **Risk-free rate**: FRED (4 week Treasury bill rate)  
- **Fama–French 3 factors (Market, SMB, HML)**: CRSP / Ken French Data Library  

**Frequency:** Monthly  
**Sample period:** 2000–2024  
**Asset universe:** Broad U.S. equity universe(large cap S&P 500)

---

## Momentum Returns (J–K Grid)

Average monthly momentum returns (t-statistics in parentheses):

| J \ K | 3 | 6 | 9 | 12 |
|-----|-----|-----|-----|-----|
| 3 | 5.03 (17.34) | 3.25 (9.52) | 2.47 (6.09) | 2.02 (4.71) |
| 6 | 2.49 (9.21) | 1.53 (4.63) | 1.15 (2.94) | 0.85 (2.05) |
| 9 | 1.68 (6.11) | 1.06 (3.40) | 0.74 (2.02) | 0.48 (1.22) |
| 12 | 1.35 (5.12) | 0.80 (2.80) | 0.49 (1.48) | 0.30 (0.83) |

Momentum profits are strongest at shorter and medium horizons, consistent with prior evidence.

---

## Factor-Based Evaluation

### CAPM (J = 6, K = 6)

| Portfolio | Alpha | Beta | t(Alpha) | R² |
|---------|-------|------|----------|----|
| Winner | 0.0194 | 1.07 | 9.91 | 0.69 |
| Loser | 0.0020 | 1.56 | 0.86 | 0.76 |
| Winner–Loser | **0.0162** | **−0.49** | **5.24** | 0.15 |

The momentum portfolio earns **statistically significant alpha** with low explanatory power from the market factor.

---

### Fama–French 3-Factor Model (Winner–Loser)

- **Alpha:** 0.0170 (t = 5.40)
- Market beta: −0.51 (significant)
- SMB, HML betas: small and insignificant
- R² ≈ 0.17

Momentum returns are **not explained by standard size and value factors**, confirming that momentum represents a distinct source of return.

---

## Risk Characteristics

Risk metrics for the J = 6, K = 6 portfolios:

| Portfolio | Annualized Volatility | Sharpe | Max Drawdown | Skew |
|---------|----------------------|--------|--------------|------|
| Winner | 19.7% | 0.125 | −47.1% | −0.17 |
| Loser | 27.9% | 0.035 | −63.4% | 0.53 |
| Momentum (W–L) | 19.6% | 0.073 | −53.5% | **−1.56** |

Key observations:
- Momentum exhibits **large drawdowns**
- Strongly **negative skewness**, indicating crash risk
- Losses are concentrated in rare but severe events

---

## Volatility Scaling

To improve risk control, the momentum portfolio is **volatility scaled**:

- Target volatility: **10% annualized**
- Volatility estimated using rolling past returns
- Position sizes scaled inversely with recent volatility
- Leverage capped to maintain realistic constraints
- Market Sharpe Ratio (same sample): **0.032**

This approach adjusts exposure dynamically without altering the underlying signal.

### Impact of Volatility Scaling

| Strategy | Volatility | Sharpe | Max Drawdown | Skew |
|--------|-----------|--------|--------------|------|
| Unscaled Momentum | 19.6% | 0.073 | −53.5% | −1.56 |
| Volatility-Scaled Momentum | **13.3%** | **0.086** | **−27.4%** | **−0.48** |

Volatility scaling:
- Cuts worst-case drawdowns by ~50%
- Reduces negative skewness substantially
- Improves risk-adjusted performance

This suggests that momentum crash risk is closely linked to periods of elevated volatility and can be mitigated through dynamic position sizing.

---

## ML-Based Momentum Crash Risk Filter

- I augment the baseline Jegadeesh–Titman (1993) momentum strategy with an ML-based crash risk classifier that predicts the probability of a momentum crash in the next month using only information available at time t.
- A crash is defined as a next-month momentum return falling in the bottom 10% of its training-sample distribution, with the threshold fixed ex ante to avoid look-ahead bias.
- Portfolio exposure is scaled smoothly as w_t = 1 - P(crash_(t+1)/X_t), reducing exposure during high crash-risk regimes.

### Features Used (All Observable at Time t)

- **Momentum state**
  - 1-month momentum return
  - 3-month rolling mean of momentum returns
  - 6-month rolling mean of momentum returns
- **Risk state**
  - 3-month rolling volatility of momentum returns
  - 6-month rolling volatility of momentum returns
  - Momentum drawdown (from rolling peak)
- **Market state**
  - Market return (1-month)
  - 3-month rolling mean of market returns
  - 6-month rolling beta of momentum returns with respect to the market

### Performance: Baseline vs ML-Filtered Momentum (Out-of-Sample)

| Strategy | Annualized Volatility | Sharpe | Max Drawdown | Skew |
|--------|----------------------|--------|--------------|------|
| Baseline Momentum | 0.1810 | 0.0958 | −0.1421 | −0.2295 |
| ML-Filtered Momentum | 0.1539 | 0.1024 | −0.1193 | −0.2850 |

The ML-based exposure filter reduces volatility by approximately **15%** and maximum drawdown by approximately **16%**, while modestly improving risk-adjusted performance as measured by the Sharpe ratio.

---