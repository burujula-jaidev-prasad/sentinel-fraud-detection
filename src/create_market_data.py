"""Generate normalized Paytm vs NIFTY 50 market time series with RBI regulatory event data."""

import os
import numpy as np
import pandas as pd

def generate_market_data():
    os.makedirs("data/market", exist_ok=True)
    os.makedirs("docs/data/market", exist_ok=True)

    # Dates from Jan 1, 2024 to Mar 28, 2024 (trading days)
    dates = pd.date_range(start="2024-01-01", end="2024-03-28", freq="B")
    n = len(dates)

    # NIFTY 50: starting around 21,740 growing steadily to ~22,320
    np.random.seed(42)
    nifty_returns = np.random.normal(0.0004, 0.006, n)
    nifty_prices = [21741.90]
    for r in nifty_returns[1:]:
        nifty_prices.append(nifty_prices[-1] * (1 + r))

    # Paytm (One97 Communications):
    # Jan 1 to Jan 30: Trading around 750-760
    # Jan 31: RBI Directive announced post-market -> Feb 1 & Feb 2: 20% lower circuit limit each day -> trades down to ~380-420
    paytm_prices = []
    base_paytm = 761.0
    
    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        if date_str < "2024-01-31":
            # Normal trading before RBI action
            daily_noise = np.random.normal(0.001, 0.015)
            base_paytm = base_paytm * (1 + daily_noise)
            paytm_prices.append(round(base_paytm, 2))
        elif date_str == "2024-01-31":
            # Event day close before full market pricing of circular
            paytm_prices.append(761.20)
        elif date_str == "2024-02-01":
            # First 20% lower circuit
            base_paytm = 761.20 * 0.80
            paytm_prices.append(round(base_paytm, 2))
        elif date_str == "2024-02-02":
            # Second 20% lower circuit
            base_paytm = base_paytm * 0.80
            paytm_prices.append(round(base_paytm, 2))
        elif date_str == "2024-02-05":
            # Further 10% decline
            base_paytm = base_paytm * 0.90
            paytm_prices.append(round(base_paytm, 2))
        elif date_str < "2024-02-20":
            daily_noise = np.random.normal(-0.005, 0.03)
            base_paytm = max(325.0, base_paytm * (1 + daily_noise))
            paytm_prices.append(round(base_paytm, 2))
        else:
            # Stabilization around ~400-420
            daily_noise = np.random.normal(0.002, 0.02)
            base_paytm = min(440.0, max(370.0, base_paytm * (1 + daily_noise)))
            paytm_prices.append(round(base_paytm, 2))

    df_market = pd.DataFrame({
        "date": [d.strftime("%Y-%m-%d") for d in dates],
        "paytm_close": paytm_prices,
        "nifty_close": [round(p, 2) for p in nifty_prices]
    })

    # Normalized series (Base = 100 on Jan 1)
    df_market["paytm_normalized"] = round(df_market["paytm_close"] / df_market["paytm_close"].iloc[0] * 100, 2)
    df_market["nifty_normalized"] = round(df_market["nifty_close"] / df_market["nifty_close"].iloc[0] * 100, 2)
    df_market["event_marker"] = df_market["date"].apply(lambda x: "RBI Directive (Jan 31)" if x == "2024-01-31" else "")

    # Calculate returns for volatility and beta
    df_market["paytm_ret"] = df_market["paytm_close"].pct_change()
    df_market["nifty_ret"] = df_market["nifty_close"].pct_change()

    # Pre-event (Jan 1 to Jan 30) vs Post-event (Feb 1 to Mar 28)
    pre_mask = df_market["date"] < "2024-01-31"
    post_mask = df_market["date"] >= "2024-02-01"

    pre_vol = float(df_market.loc[pre_mask, "paytm_ret"].std() * np.sqrt(252) * 100)
    post_vol = float(df_market.loc[post_mask, "paytm_ret"].std() * np.sqrt(252) * 100)

    # Beta = Cov(Rp, Rn) / Var(Rn)
    cov_pre = np.cov(df_market.loc[pre_mask, "paytm_ret"].dropna(), df_market.loc[pre_mask, "nifty_ret"].dropna())[0, 1]
    var_nifty_pre = df_market.loc[pre_mask, "nifty_ret"].var()
    beta_pre = float(cov_pre / var_nifty_pre) if var_nifty_pre > 0 else 1.15

    cov_post = np.cov(df_market.loc[post_mask, "paytm_ret"].dropna(), df_market.loc[post_mask, "nifty_ret"].dropna())[0, 1]
    var_nifty_post = df_market.loc[post_mask, "nifty_ret"].var()
    beta_post = float(cov_post / var_nifty_post) if var_nifty_post > 0 else 2.40

    df_market["pre_volatility"] = round(pre_vol, 2)
    df_market["post_volatility"] = round(post_vol, 2)
    df_market["beta_pre"] = round(beta_pre, 2)
    df_market["beta_post"] = round(beta_post, 2)

    for path in ["data/market/paytm_nifty.csv", "docs/data/market/paytm_nifty.csv"]:
        df_market.to_csv(path, index=False)
        print(f"Exported market data to {path} (Rows: {len(df_market)})")

if __name__ == "__main__":
    generate_market_data()
