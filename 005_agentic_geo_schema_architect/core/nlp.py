import spacy
import subprocess
import sys

class EntityExtractor:
    def __init__(self):
        self.nlp = None
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback to Regex-based extraction if model cannot be downloaded
            pass

    def extract_relationships(self, text: str):
        if self.nlp:
            doc = self.nlp(text[:10000])
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "description": spacy.explain(ent.label_)
                })
            return entities
        else:
            # Simple Regex Fallback for Persons, Orgs, and URLs
            import re
            entities = []
            
            # Match potential Organizations (Capitalized words)
            orgs = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text[:5000])
            for org in list(set(orgs))[:10]: # Limit results
                entities.append({
                    "text": org,
                    "label": "ORG/PERSON",
                    "description": "Extracted via Regex (Offline Mode)"
                })
            
            return entities
