# NLP Sentiment Trading using FinBERT

![Python](https://img.shields.io/badge/Python-3.11%2B-blue) ![NLP](<https://img.shields.io/badge/NLP-Transformers%20(BERT)-orange>) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![License](https://img.shields.io/badge/License-MIT-green)

## Executive Summary

This project is a real-time **Event-Driven Trading System** that utilizes **Natural Language Processing (NLP)** to quantify market sentiment. Unlike traditional price-action bots, this engine scrapes unstructured financial news, processes it using **FinBERT** (a Transformer model pre-trained on financial texts), and generates trade signals based on the aggregate "Mood" of the market.

The system features a live **Streamlit Dashboard** for monitoring news flow and a **Vectorized Backtesting Engine** to validate the predictive power of sentiment on asset prices.

### 1\. Data Ingestion (The Scraper)

- **Source:** FinViz (Financial Visualizations).
- **Logic:** Custom-built `NewsScraper` class capable of parsing HTML tables and handling missing timestamps (forward-filling dates from previous rows).
- **Anti-Blocking:** Mimics browser headers (`User-Agent`) to bypass basic 403 Forbidden protections.

### 2\. The AI Core (FinBERT)

We utilize **FinBERT** (ProsusAI), a BERT model fine-tuned on a corpus of 4.9 million financial documents.

- **Architecture:** 12-layer Transformer encoder.
- **Tokenization:** WordPiece embeddings optimized for financial lexicon (e.g., distinguishing "Vice" as neutral vs. negative).
- **Optimization:** Implements a **Singleton Pattern** to load the 440MB model into memory (or VRAM) only once, enabling millisecond-latency for subsequent inference calls.
- **Hardware Acceleration:** Auto-detects **NVIDIA CUDA** to run inference on the GPU.

### 3\. Signal Generation Logic

Sentiment scores ($S$) are aggregated daily to form a trade signal:

$$ S*{daily} = \frac{1}{N} \sum*{i=1}^{N} \text{Confidence}\_i \times \text{Label}\_i $$

Where $\text{Label} \in \{+1, 0, -1\}$.

- **Long Signal:** $S_{daily} > 0.2$
- **Short Signal:** $S_{daily} < -0.2$
- **Neutral:** $-0.2 \le S_{daily} \le 0.2$

## Dashboard Features

The project includes a fully interactive web terminal built with **Streamlit**:

- **Real-Time Feed:** Live table of headlines color-coded by AI sentiment.
- **Price Overlay:** Plotly candlestick charts overlaid with sentiment indicators.
- **Data Collection:** Automatically saves analyzed news to `data/news_db.csv` to build a proprietary dataset for future research.

_(Note: Run `streamlit run app/main.py` to launch)_

## System Architecture

The application follows a modular "Data Pipeline" architecture, moving from raw web scraping to deep learning inference to strategy execution.

```mermaid
graph LR
    A[FinViz News Stream] -->|Scraper| B(Raw Headlines)
    B -->|Tokenization| C{FinBERT AI}
    C -->|Inference (GPU)| D[Sentiment Scores]
    D -->|Aggregation| E[Signal Generation]
    E -->|Backtest| F[Equity Curve]
    D -->|Live Feed| G[Streamlit Dashboard]
```

## Getting Started

### Prerequisites

- Python 3.8+
- PyTorch (with CUDA support recommended for GPU acceleration)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/JayGupta2003/NLP-Sentiment-Trading.git
    cd NLP-Sentiment-Trading
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard:**

    ```bash
    streamlit run app/main.py
    ```

4.  **Run the Research Backtest:**
    Open `notebooks/lab_backtest.ipynb` to verify strategy performance on historical data once gathered.

## Tech Stack

- **Transformers (Hugging Face):** FinBERT model implementation.
- **PyTorch:** Deep learning backend.
- **Streamlit:** Web UI framework.
- **BeautifulSoup4:** Web scraping.
- **Pandas/Plotly:** Data manipulation and visualization.

## Disclaimer

This tool provides sentiment analysis based on news headlines. It does not constitute financial advice. Deep learning models can hallucinate or misinterpret context. Use at your own risk.

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
