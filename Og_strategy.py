import yfinance as yf
import pandas as pd
import numpy as np
import ta

tickers = {
    "VBL": "VBL.NS",
    "Trent": "TRENT.NS",
    "TCS": "TCS.NS",
    "DIVISLAB": "DIVISLAB.NS",
    "SBIN": "SBIN.NS",
    "BAJAJ_FINANCE": "BAJFINANCE.NS",
    "FIRSTCRY": "FIRSTCRY.NS",
    "ETERNAL": "ETERNAL.NS"
}

def fetch_data(ticker):
    raw = yf.download(ticker, interval='15m', period='30d', progress=False)

    # Fix: convert columns to 1D Series
    df = pd.DataFrame({
        'Open': raw['Open'].squeeze(),
        'High': raw['High'].squeeze(),
        'Low': raw['Low'].squeeze(),
        'Close': raw['Close'].squeeze(),
        'Volume': raw['Volume'].squeeze()
    })
    return df

def apply_strategy(df):
    df = df.copy()

    # Technical Indicators
    bb = ta.volatility.BollingerBands(close=df['Close'], window=30, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_mid'] = bb.bollinger_mavg()

    df['rsi'] = ta.momentum.RSIIndicator(close=df['Close'], window=21).rsi()
    df.dropna(inplace=True)

    # Entry Conditions
    df['long_signal'] = (df['Close'] < df['bb_lower']) & (df['rsi'] < 30)
    df['short_signal'] = (df['Close'] > df['bb_upper']) & (df['rsi'] > 70)

    # Backtesting Logic
    trades = []
    position = None

    for i in range(5, len(df) - 1):
        if position is None:
            if df['long_signal'].iloc[i]:
                entry = df['Close'].iloc[i + 1]
                sl = df['Low'].iloc[i-5:i+1].min()
                target = df['bb_mid'].iloc[i]
                rr = 1.5
                exit_price = min(target, entry + rr * (entry - sl))
                trades.append({'Type': 'Long', 'Entry': entry, 'Exit': exit_price, 'Return': (exit_price - entry)/entry})
                position = 'entered'
            elif df['short_signal'].iloc[i]:
                entry = df['Close'].iloc[i + 1]
                sl = df['High'].iloc[i-5:i+1].max()
                target = df['bb_mid'].iloc[i]
                rr = 1.5
                exit_price = max(target, entry - rr * (sl - entry))
                trades.append({'Type': 'Short', 'Entry': entry, 'Exit': exit_price, 'Return': (entry - exit_price)/entry})
                position = 'entered'
        if position:
            position = None

    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        return {
            'Win Rate (%)': 0,
            'Avg Return (%)': 0,
            'Trades': 0,
            'Profit Factor': 0
        }

    trades_df['Win'] = trades_df['Return'] > 0
    gross_profit = trades_df.loc[trades_df['Win'], 'Return'].sum()
    gross_loss = abs(trades_df.loc[~trades_df['Win'], 'Return'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else np.nan

    return {
        'Win Rate (%)': round(trades_df['Win'].mean() * 100, 2),
        'Avg Return (%)': round(trades_df['Return'].mean() * 100, 2),
        'Trades': len(trades_df),
        'Profit Factor': round(profit_factor, 2)
    }

# Run Backtests
results = {}
for name, symbol in tickers.items():
    try:
        print(f"🔄 Backtesting {name}...")
        df = fetch_data(symbol)
        if not df.empty:
            results[name] = apply_strategy(df)
        else:
            results[name] = "No data available"
    except Exception as e:
        results[name] = f"Error: {e}"

# Display Results
print("\n📊 Final Backtest Results:\n")
for stock, result in results.items():
    print(f"{stock}: {result}")

# Export Results to CSV
filtered_results = {k: v for k, v in results.items() if isinstance(v, dict)}
results_df = pd.DataFrame.from_dict(filtered_results, orient='index')
results_df.index.name = 'Stock'
results_df.to_csv("backtest_results.csv")
print("\n✅ Results exported to 'backtest_results.csv'")
    
