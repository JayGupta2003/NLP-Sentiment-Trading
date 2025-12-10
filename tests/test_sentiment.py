import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sentiment import SentimentAnalyzer #type: ignore

nlp = SentimentAnalyzer()

test_headlines = [
    "NVIDIA beats earnings estimates by 15%",  # Obviously Good
    "NVIDIA production halted due to chip shortage", # Obviously Bad
    "NVIDIA announces new Vice President of Sales", # Neutral (Trick: 'Vice' is usually bad in generic NLP)
    "Fed keeps interest rates unchanged", # Neutral/Mixed
    "Operating expenses increased, but margins expanded" # Complex (Bad then Good)
]

print("\n--- AI ANALYSIS ---")
results = nlp.analyze_headlines(test_headlines)
print(results[['Headline', 'Label', 'Confidence', 'Sentiment_Score']])

"""Output:
Loading FinBERT Model...
Device set to use cpu
FinBERT Model Loaded!

--- AI ANALYSIS ---
                                            Headline     Label  Confidence  Sentiment_Score
0             NVIDIA beats earnings estimates by 15%  positive    0.825405         0.825405
1      NVIDIA production halted due to chip shortage  negative    0.953405        -0.953405
2       NVIDIA announces new Vice President of Sales   neutral    0.911593         0.000000
3                 Fed keeps interest rates unchanged   neutral    0.874370         0.000000
4  Operating expenses increased, but margins expa...  positive    0.909979         0.909979
"""