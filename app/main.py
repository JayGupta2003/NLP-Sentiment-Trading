import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import NewsScraper
from src.sentiment import SentimentAnalyzer
from src.data_manager import DataManager

st.set_page_config(page_title="FinBERT Sentiment Trading", layout="wide")
st.title("FinBERT AI Trading")

# We use @st.cache_resource so we only load the heavy AI model ONCE.
@st.cache_resource
def load_model():
    return SentimentAnalyzer()

@st.cache_resource
def load_scraper():
    return NewsScraper()

model = load_model()
scraper = load_scraper()

with st.sidebar:
    st.header("Control Panel")
    ticker = st.text_input("Enter Ticker", value="NVDA").upper()
    days_back = st.slider("Lookback Days", min_value=1, max_value=7, value=3)
    
    if st.button("Analyze Sentiment"):
        st.session_state['run_analysis'] = True

if st.session_state.get('run_analysis', False):
    # 1. Fetch News
    st.subheader(f"Analyzing Real-Time News for {ticker}...")
    with st.spinner("Scraping headlines..."):
        news_df = scraper.get_news(ticker)
    
    if news_df.empty:
        st.error(f"No news found for {ticker}. Try a popular stock like AAPL or TSLA.")
    else:
        # 2. Analyze Sentiment
        with st.spinner("Running FinBERT..."):
            # Filter by date if needed, but for now we take all scraped news
            scored_df = model.analyze_headlines(news_df['Headline'].tolist())

            # Merge Sentiment back into News Data
            full_df = pd.concat([news_df, scored_df[['Label', 'Confidence', 'Sentiment_Score']]], axis=1)

            dm = DataManager()
            dm.save_news(full_df)
            st.success(f"Saved {len(full_df)} headlines to database!")

        # 3. Dashboard Layout
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### Latest Headlines")
            # Style the dataframe: Green for Pos, Red for Neg
            def color_sentiment(val):
                color = 'green' if val > 0 else 'red' if val < 0 else 'gray'
                return f'color: {color}'
            
            display_df = full_df[['Date', 'Time', 'Headline', 'Sentiment_Score']].head(10)
            st.dataframe(display_df.style.map(color_sentiment, subset=['Sentiment_Score']), hide_index=True)

            # Aggregate Sentiment
            avg_sentiment = full_df['Sentiment_Score'].mean()
            sentiment_label = "BULLISH" if avg_sentiment > 0.1 else "BEARISH" if avg_sentiment < -0.1 else "NEUTRAL"
            color = "green" if avg_sentiment > 0 else "red" 

            st.metric("Aggregate Sentiment Score", f"{avg_sentiment:.2f}", delta=sentiment_label)
        
        with col2:
            st.markdown("### Price vs Sentiment Overlay")

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back + 2)
            prices = yf.download(ticker, start=start_date, end=end_date, interval='15m', progress=False)

            if isinstance(prices.columns, pd.MultiIndex):
                prices.columns = prices.columns.get_level_values(0)
                prices = prices.dropna()

            if not prices.empty:
                # Create Dual-Axis Chart
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                # Add Price Candle/Line
                fig.add_trace(go.Candlestick(x=prices.index,
                                open=prices['Open'],
                                high=prices['High'],
                                low=prices['Low'],
                                close=prices['Close'],
                                name="Price"), secondary_y=False)
                fig.update_layout(title=f"{ticker} 15m Price Action", xaxis_title="Date", height=500)
                st.plotly_chart(fig, width='stretch')
            else:
                st.error(f"No price data found for {ticker}.")
        
        # 4. Deep Dive Charts
        st.markdown("---")
        st.markdown("### FinBERT Confidence Distribution")
        
        # Histogram of Sentiment Scores
        fig_hist = go.Figure(data=[go.Histogram(x=full_df['Sentiment_Score'], nbinsx=20)])
        fig_hist.update_layout(title="Distribution of News Sentiment (Right = Good, Left = Bad)")
        st.plotly_chart(fig_hist, width='stretch')

else:
    st.info("Enter a ticker and click 'Analyze Sentiment' to start.")