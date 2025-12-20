## Momentum Strategy Replication (Jegadeesh & Titman, 1993)

This project implements a momentum-based trading strategy inspired by Jegadeesh and Titman (1993), which documents short- to medium-term continuation in stock returns.

NOTE: Due to the proprietary nature of CRSP data, this replication uses publicly available stock price data from Yahoo Finance and focuses on replicating the methodology rather than exact return magnitudes.

The project is structured as a reproducible research pipeline with separate modules for data loading, portfolio construction, and performance evaluation.

---

## Strategy Overview

The momentum strategy is constructed as follows:

- **J (Formation Period):**  
  Stocks are ranked based on their cumulative returns over the past *J* months.

- **K (Holding Period):**  
  Portfolios formed based on the ranking are held for *K* months.

At each formation date, stocks are sorted into deciles based on past
*J*-month returns. A **winner portfolio** is formed from the top decile,
and a **loser portfolio** from the bottom decile. The momentum strategy
goes long winners and short losers.

Portfolios are held with **overlapping holding periods**, meaning that
at any point in time, multiple portfolios formed in previous months are
simultaneously active.

---

## Project Structure

data/ # Raw and processed data
src/ # Core Python modules
notebooks/ # Analysis and experimentation
results/ # Tables and plots