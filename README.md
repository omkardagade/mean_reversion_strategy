📄 Report: Learnings from Algorithmic Trading using Python and C++ integration (ID:86)

📌 Introduction

In this project, I utilized and implemented a rule-based backtesting framework to backtest a simple but sound intraday trading strategy. The backtesting framework backtested a range of stocks listed on the Indian stock exchange based on data at 15-minute intervals over a 30-day time span. The primary objective was to identify long and short opportunities by using a combination of technical indicators like Bollinger Bands and RSI.

⸻

🧠 Key Learnings

1. 📈 Financial Markets and Indicators
	•	Bollinger Bands: I learned how Bollinger Bands can be used to identify volatility extremes. Specifically:
	•	Price falling below the lower band might indicate oversold conditions (buy signal).
	•	Price rising above the upper band might indicate overbought conditions (sell signal).
	•	RSI (Relative Strength Index): Helped me filter high-probability trade setups by confirming overbought/oversold signals.
	•	Combining Indicators: I understood that using multiple indicators together (like BB and RSI) can reduce false signals and improve strategy robustness.

⸻

2. 🧪 Backtesting Concepts
	•	Strategy Logic: I built logic to simulate both long and short trades based on entry signals and computed returns.
	•	Risk-Reward Calculation: I applied a risk-to-reward ratio of 1:1.5 to simulate realistic trade exits using dynamically calculated stop-loss levels based on recent price extremes.
	•	Performance Metrics:
	•	Win Rate: Percentage of trades that were profitable.
	•	Average Return: Mean return per trade.
	•	Profit Factor: Ratio of gross profits to gross losses, which helped measure the efficiency of the strategy.

⸻

3. 🧠 Python & Libraries
	•	pandas: For data manipulation, rolling windows, and signal creation.
	•	yfinance: For downloading historical stock price data at 15-minute intervals.
	•	ta (Technical Analysis library): To compute indicators like RSI and Bollinger Bands with ease.
	•	Exception Handling: Used try-except blocks to ensure the system doesn’t break when data is missing or APIs fail.

⸻

4. ⚙️ Algorithm Design
	•	Built a modular structure with reusable functions: fetch_data() and apply_strategy().
	•	Implemented a simple position management system to prevent overlapping trades.
	•	Ensured that trades were based on confirmed signals and exited with a clear logic using stoploss and target estimation.

⸻

5. 📁 Data Handling and Reporting
	•	Exported results using pandas.DataFrame.to_csv() to create:
	•	backtest_results.csv: For an overview of strategy performance per stock.
	•	Learned how to handle missing or incomplete data for specific tickers gracefully.
	•	Developed a clean and readable terminal output for fast diagnostics and iteration.

⸻

🔍 Challenges Faced
	•	Initially, I struggled with understanding the proper way to simulate trade exits and implement stoploss-based calculations.
	•	Another issue was handling position overlap—if not properly coded, multiple signals would trigger multiple entries.
	•	Additionally, I had to tune the signal thresholds to find a balance between signal quantity and quality.

⸻

✅ Outcomes

By the end of this project:
  • I gained a basic knowledge of quantitative strategy formulation. 
  • I wrote an operational backtest engine from scratch using real data. 
  • Enhanced confidence in using Python for financial data analysis and prototyping of strategies. 
  • I outlined some areas of future development: including the addition of position sizing, multi-bar exits, and live trading hooks.
