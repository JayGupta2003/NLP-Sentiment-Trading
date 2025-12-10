import torch
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        """
        Singleton class to load FinBERT once.
        Using the 'prosusai/finbert' model which is the industry standard.
        """
        print("Loading FinBERT Model...")
        if torch.cuda.is_available():
            self.device = 0 
            print("NVIDIA GPU (CUDA) Detected!")
        else:
            self.device = -1
            print("No GPU detected")
        self.tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
        self.model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

        # Create a Hugging Face pipeline for easy usage
        # This handles tokenization, forward pass, and softmax automatically
        self.nlp = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        print("FinBERT Model Loaded!")

    def analyze_headlines(self, headlines):
        """
        Batch processes a list of headlines and returns sentiment scores.
        """
        if not headlines:
            return []
        
        # The pipeline returns a list of dicts: [{'label': 'positive', 'score': 0.95}, ...]
        results = self.nlp(headlines)
        processed_data = []

        for i, res in enumerate(results):
            label = res['label']
            confidence = res['score']

            # Convert label to a numerical score for plotting
            # Positive = 1, Neutral = 0, Negative = -1
            # Multiplying by confidence to get a "Weighted Score"
            if label == 'positive':
                score = confidence
            elif label == 'negative':
                score = -confidence
            else:
                score = 0.0

            processed_data.append({
                'Headline': headlines[i],
                'Label': label,
                'Confidence': confidence,
                'Sentiment_Score': score
            })
        return pd.DataFrame(processed_data)