from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

class BiasAnalyzer:
    def __init__(self):
        self.model = None

    def _ensure_model(self):
        """Lazy load the model only when needed."""
        if self.model is None:
            try:
                # Use a very small model for maximum speed
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"SBERT Load Error: {e}")
                self.model = "FAILED"

    def calculate_divergence(self, text_a, text_b):
        """Calculates Semantic Divergence between two model responses."""
        self._ensure_model()
        
        if self.model == "FAILED" or self.model is None:
            return 0.5 # Fallback
            
        try:
            emb_a = self.model.encode(text_a, convert_to_tensor=True)
            emb_b = self.model.encode(text_b, convert_to_tensor=True)
            similarity = util.cos_sim(emb_a, emb_b).item()
            return max(0.0, min(1.0, 1.0 - similarity))
        except:
            return 0.5

    def get_heatmap_data(self, text, keywords):
        """Identify which keywords are most salient in the text."""
        salience = {}
        for kw in keywords:
            count = len(text.lower().split(kw.lower())) - 1
            salience[kw] = count
        return salience
