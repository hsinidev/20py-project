import pandas as pd
import numpy as np

class RiskMatrix:
    """
    Vectorized Risk Scoring Logic for organizational departments.
    """
    def __init__(self):
        self.departments = ["HR", "Finance", "IT", "Operations", "Sales", "Executive"]
        self.risk_data = pd.DataFrame(columns=["department", "entities_count", "vuln_count", "avg_risk"])

    def aggregate_data(self, scan_results):
        """
        Processes a list of scan results: [{'department': 'HR', 'nlp_results': {...}}, ...]
        """
        temp_data = []
        for res in scan_results:
            nlp = res['nlp_results']
            temp_data.append({
                "department": res.get("department", "Unknown"),
                "entities_count": len(nlp['entities']),
                "vuln_count": len(nlp['vulnerabilities']),
                "avg_risk": nlp['risk_score']
            })
        
        self.risk_data = pd.DataFrame(temp_data)
        return self.calculate_matrix()

    def calculate_matrix(self):
        if self.risk_data.empty:
            return pd.DataFrame()
            
        # Group by department and calculate mean risk
        matrix = self.risk_data.groupby("department").agg({
            "avg_risk": "mean",
            "entities_count": "sum",
            "vuln_count": "sum"
        }).reset_index()
        
        # Sort by highest risk
        matrix = matrix.sort_values(by="avg_risk", ascending=False)
        return matrix

    def get_heatmap_data(self):
        """Prepares data for Plotly/HoloViews heatmaps."""
        matrix = self.calculate_matrix()
        if matrix.empty:
            return {"z": [], "x": [], "y": []}
            
        return {
            "z": [matrix["avg_risk"].tolist()],
            "x": matrix["department"].tolist(),
            "y": ["Social Vulnerability Index"]
        }

if __name__ == "__main__":
    rm = RiskMatrix()
    sample_scan = [
        {"department": "HR", "nlp_results": {"entities": [1,2,3], "vulnerabilities": [1], "risk_score": 0.5}},
        {"department": "Finance", "nlp_results": {"entities": [1], "vulnerabilities": [1,2], "risk_score": 0.7}},
        {"department": "IT", "nlp_results": {"entities": [1,2], "vulnerabilities": [], "risk_score": 0.2}},
    ]
    print(rm.aggregate_data(sample_scan))
