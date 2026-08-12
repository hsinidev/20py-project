from transformers import pipeline
import torch
from .models import SentimentResult

class FramingClassifier:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load DistilBERT for sentiment
        try:
            self.sentiment_pipe = pipeline("sentiment-analysis", 
                                          model="distilbert-base-uncased-finetuned-sst-2-english",
                                          device=self.device)
        except Exception:
            self.sentiment_pipe = None

    def analyze(self, text: str) -> SentimentResult:
        if not self.sentiment_pipe:
            return SentimentResult(0.0, "NEU", "Generic", 0.0)

        res = self.sentiment_pipe(text[:512])[0]
        score = 0.8 if res['label'] == 'POSITIVE' else -0.8
        score *= res['score']
        
        # Heuristic Framing Detection (Beyond simple sentiment)
        framing = "General Information"
        text_lower = text.lower()
        
        # Framing rules
        if any(w in text_lower for w in ["premium", "luxury", "elite", "leader", "pioneer"]):
            framing = "Premium Leader"
        elif any(w in text_lower for w in ["cheap", "budget", "affordable", "alternative", "basic"]):
            framing = "Budget Alternative"
        elif any(w in text_lower for w in ["complex", "technical", "advanced", "specialized"]):
            framing = "Technical Authority"
        elif any(w in text_lower for w in ["reliable", "standard", "popular", "common"]):
            framing = "Market Standard"

        return SentimentResult(
            score=score,
            label=res['label'],
            framing=framing,
            confidence=res['score']
        )
