import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scraper import NewsScraper #type: ignore

scraper = NewsScraper()
df = scraper.get_news("NVDA")

print("\n--- HEADLINES SAMPLE ---")
print(df[['Date', 'Time', 'Headline']].head())

print("\n--- BATCH TEST ---")
watchlist = ['AAPL', 'TSLA', 'AMD']
batch_df = scraper.get_news_batch(watchlist)
print(f"Total Headlines Fetched: {len(batch_df)}")

"""Output:
Scanning news for NVDA...
Found 100 headlines for NVDA

--- HEADLINES SAMPLE ---
    Date     Time                                           Headline
0  Today  05:15PM  Nvidia Rises As Trump OKs H200 AI Chip Sales I...
1  Today  05:15PM  Dow Jones Futures: Astera, Netflix, Nvidia, Te...
2  Today  05:09PM  Trump allows Nvidia to ship H200 chips to Chin...
3  Today  05:06PM  Trump Approves Sale of Nvidia's H200 AI Chip t...
4  Today  04:58PM  Trump green-lights Nvidia selling H200 chips t...

--- BATCH TEST ---
Scanning news for AAPL...
Found 100 headlines for AAPL
Scanning news for TSLA...
Found 100 headlines for TSLA
Scanning news for AMD...
Found 100 headlines for AMD
Total Headlines Fetched: 300
"""