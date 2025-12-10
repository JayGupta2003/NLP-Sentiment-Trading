import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import io

#Using FinViz to gather news as it aggregates major news outlets
class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://finviz.com/quote.ashx?t='

    def get_news(self, ticker):
        """
        Scrapes recent news headlines for a specific ticker from FinViz.
        Returns: DataFrame [Ticker, Date, Time, Headline, Link]
        """
        url = self.base_url + ticker
        print(f"Scanning news for {ticker}...")

        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # FinViz stores news in a specific div id='news-table'
            news_table = soup.find(id='news-table')

            if not news_table:
                print(f"No news found for {ticker}.")
                return pd.DataFrame()
            
            parsed_data = []

            # Iterate through all rows (tr) in the table
            for row in news_table.findAll('tr'):
                # The 'a' tag contains the Headline and Link
                a_tag = row.find('a')
                if not a_tag:
                    continue

                headline = a_tag.text
                link = a_tag['href']

                # The 'td' tag contains the timestamp info
                timestamp_data = row.td.text.split()

                # Logic to handle the "Missing Date" issue
                if len(timestamp_data) == 1:
                    # Case: "09:30AM" (Uses date from previous row)
                    time = timestamp_data[0]
                    # date stays the same as variable 'date' from previous loop
                else:
                    # Case: "Dec-09-23 09:30AM" (New Date)
                    date = timestamp_data[0]
                    time = timestamp_data[1]
                
                parsed_data.append([ticker, date, time, headline, link])

            # Create DataFrame
            columns = ['Ticker', 'Date', 'Time', 'Headline', 'Link']
            df = pd.read_csv(io.StringIO(""), names=columns) if not parsed_data else pd.DataFrame(parsed_data, columns=columns)

            if not df.empty:
                # Clean up Date format to proper datetime objects later if needed
                print(f"Found {len(df)} headlines for {ticker}")
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error scraping for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_news_batch(self, tickers):
        """
        Scrapes news for a list of tickers and combines them.
        """
        all_news = []
        for i in tickers:
            df = self.get_news(i)
            all_news.append(df)
        
        if all_news:
            return pd.concat(all_news, ignore_index=True)
        return pd.DataFrame()