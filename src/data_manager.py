import pandas as pd
import os

class DataManager:
    def __init__(self, db_path='../data/news_db.csv'):
        self.db_path = db_path
        self.ensure_directory()

    def ensure_directory(self):
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        
    def save_news(self, news_df):
        """
        Appends new scraped news to the master CSV, avoiding duplicates.
        """
        if news_df.empty:
            return

        if os.path.exists(self.db_path):
            existing_df = pd.read_csv(self.db_path)
            combined = pd.concat([existing_df, news_df])
            combined = combined.drop_duplicates(subset=['Ticker', 'Date', 'Time', 'Headline'])
        else:
            combined = news_df

        # Save
        combined.to_csv(self.db_path, index=False)
        print(f"💾 Saved {len(news_df)} rows. Total DB Size: {len(combined)} rows.")

    def load_data_for_ticker(self, ticker):
        """
        Returns all historical news for a specific ticker.
        """
        if not os.path.exists(self.db_path):
            return pd.DataFrame()
        
        df = pd.read_csv(self.db_path)
        return df[df['Ticker'] == ticker].copy()