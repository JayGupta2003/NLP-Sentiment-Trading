import pandas as pd
import numpy as np
import yfinance as yf

class Strategy:
    def __init__(self, ticker, sentiment_df, initial_capital=10000):
        self.ticker = ticker
        self.news = sentiment_df
        self.capital = initial_capital

    def preprocess_sentiment(self):
        """
        Aggregates multiple headlines into a single Daily Sentiment Score.
        """
        self.news['Date'] = pd.to_datetime(self.news['Date']).dt.date
        
        # Group by Date and calculate Mean Sentiment
        daily_sentiment = self.news.groupby('Date')['Sentiment_Score'].mean().reset_index()
        daily_sentiment = daily_sentiment.set_index('Date')
        return daily_sentiment

    def run_backtest(self):
        """
        Merges sentiment with price data and calculates returns.
        """
        daily_scores = self.preprocess_sentiment()
        
        if daily_scores.empty:
            print("No sentiment data to backtest.")
            return pd.DataFrame()

        start_date = daily_scores.index.min()
        end_date = pd.to_datetime('today').date()
        
        # Download prices
        prices = yf.download(self.ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
        
        if prices.empty:
            return pd.DataFrame()
        
        if isinstance(prices.columns, pd.MultiIndex):
            prices.columns = prices.columns.get_level_values(0)

        # Merge Data (Align Price and Sentiment)
        # We perform a Left Join on Price Index to keep all trading days
        analysis_df = prices[['Open', 'Close']].copy()
        analysis_df.index = analysis_df.index.date 

        merged = analysis_df.join(daily_scores)
        
        merged['Sentiment_Score'] = merged['Sentiment_Score'].fillna(0.0)

        # Generate Signals
        # If Sentiment > 0.2, Buy. If < -0.2, Short.
        merged['Signal'] = 0
        merged.loc[merged['Sentiment_Score'] > 0.2, 'Signal'] = 1
        merged.loc[merged['Sentiment_Score'] < -0.2, 'Signal'] = -1
        
        # Calculate Returns
        # We trade at the OPEN of the NEXT day based on TODAY's sentiment
        # Or simpler: We hold for the day. Let's do: Position * Daily_Return
        merged['Daily_Return'] = merged['Close'].pct_change()
        
        # Shift signal by 1 day (Avoid Lookahead Bias)
        # We react to the news the NEXT day
        merged['Position'] = merged['Signal'].shift(1)
        
        merged['Strategy_Return'] = merged['Position'] * merged['Daily_Return']
        merged['Cumulative_Return'] = (1 + merged['Strategy_Return'].fillna(0)).cumprod() * self.capital
        
        return merged