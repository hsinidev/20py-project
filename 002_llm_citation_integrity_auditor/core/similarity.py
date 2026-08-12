import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import difflib

class SimilarityEngine:
    _model = None

    @classmethod
    def load(cls):
        try:
            from sentence_transformers import SentenceTransformer
            if cls._model is None:
                cls._model = SentenceTransformer('all-MiniLM-L6-v2')
            return True
        except ImportError:
            return False

    @classmethod
    def get_score(cls, claim: str, source_text: str) -> float:
        """Computes semantic similarity between claim and source."""
        if not source_text or "Error" in source_text or "Failure" in source_text:
            return 0.0
        
        if cls._model:
            embeddings = cls._model.encode([claim, source_text])
            return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
        
        # Jaccard Fallback
        c_set = set(claim.lower().split())
        s_set = set(source_text.lower().split())
        if not c_set: return 0.0
        return len(c_set.intersection(s_set)) / len(c_set)

    @classmethod
    def generate_diff(cls, claim: str, source_context: str) -> str:
        """Generates an HTML diff highlighting contradictions or support."""
        # Simple character-based diff for visualization
        d = difflib.HtmlDiff()
        return d.make_table(claim.splitlines(), source_context.splitlines()[:5], context=True, numlines=1)
