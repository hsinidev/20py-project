import spacy
import re
import logging

class SocialNLP:
    """
    Cognitive Analysis Layer for detecting PII and Social Engineering vulnerabilities.
    """
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            logging.warning(f"Spacy model {model} not found. Using empty analyzer fallback.")
            self.nlp = None

        # Custom patterns for technical vulnerabilities
        self.vuln_patterns = {
            "internal_tech": r"(internal|proprietary|private)\s+(system|server|db|database|infrastructure)",
            "deadline": r"(deadline|due by|launching on|release date)\s+(\w+\s+\d+)",
            "location": r"(at our|visit us at|working from)\s+(office|branch|street|building)",
            "credentials": r"(password|secret|api key|token|key)\s*[:=]\s*",
        }

    def analyze_text(self, text):
        if not self.nlp:
            return {"entities": [], "vulnerabilities": [], "risk_score": 0.0}

        doc = self.nlp(text)
        results = {
            "entities": [],
            "vulnerabilities": [],
            "risk_score": 0.0
        }

        # Entity Extraction (PII)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "DATE", "PHONE_NUMBER"]:
                results["entities"].append({"text": ent.text, "label": ent.label_})

        # Pattern Matching for Social Engineering
        for vuln_type, pattern in self.vuln_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                results["vulnerabilities"].append({
                    "type": vuln_type,
                    "count": len(matches),
                    "description": f"Potential leakage of {vuln_type.replace('_', ' ')}"
                })

        # Calculate base Risk Score
        risk = (len(results["entities"]) * 0.1) + (len(results["vulnerabilities"]) * 0.2)
        results["risk_score"] = min(1.0, risk)

        return results

if __name__ == "__main__":
    # Test
    analyzer = SocialNLP()
    sample = "I'm John Doe working at our New York office. Our internal server 'PROD-DB' has a deadline on May 20th."
    res = analyzer.analyze_text(sample)
    print(f"Risk Score: {res['risk_score']}")
    print(f"Entities: {res['entities']}")
    print(f"Vulns: {res['vulnerabilities']}")
