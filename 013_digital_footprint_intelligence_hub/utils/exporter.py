import json
import csv
import os
from datetime import datetime

class ReportExporter:
    """
    Export Engine for intelligence dossiers.
    Supports JSON, CSV, and formatted text (simulated PDF logic).
    """
    @staticmethod
    def to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return filename

    @staticmethod
    def to_csv(data, filename):
        if not data:
            return None
        
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        return filename

    @staticmethod
    def to_pdf_sim(data, filename, target_name):
        """
        Simulates PDF report generation using a structured Markdown/Text format.
        In a full implementation, reportlab or fpdf would be used.
        """
        report_content = []
        report_content.append("="*60)
        report_content.append(f"DIGITAL FOOTPRINT INTELLIGENCE DOSSIER")
        report_content.append(f"Target: {target_name}")
        report_content.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append("="*60)
        report_content.append("\n[DISCOVERED ACCOUNTS]\n")
        
        accounts = data.get('accounts', [])
        for acc in accounts:
            report_content.append(f"- {acc['platform']}: {acc['url']}")
            
        report_content.append("\n[DORKING RESULTS]\n")
        dorks = data.get('dorks', [])
        for dork in dorks:
            report_content.append(f"Query: {dork['query']}")
            report_content.append(f"Title: {dork['title']}")
            report_content.append(f"URL: {dork['url']}")
            report_content.append("-" * 30)

        report_content.append("\n" + "="*60)
        report_content.append("CONFIDENTIAL - FOR AUTHORIZED USE ONLY")
        report_content.append("Developed by HSINI MOHAMED")
        report_content.append("="*60)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        return filename

def generate_report(data, base_path, target_name, formats=['json', 'csv', 'pdf']):
    exporter = ReportExporter()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}

    if 'json' in formats:
        fname = os.path.join(base_path, f"dossier_{target_name}_{timestamp}.json")
        results['json'] = exporter.to_json(data, fname)
    
    if 'csv' in formats:
        fname = os.path.join(base_path, f"dossier_{target_name}_{timestamp}.csv")
        # Flatten data for CSV if it's nested
        csv_data = data.get('accounts', []) + data.get('dorks', [])
        results['csv'] = exporter.to_csv(csv_data, fname)

    if 'pdf' in formats:
        fname = os.path.join(base_path, f"dossier_{target_name}_{timestamp}.txt") # Using .txt for demo simplicity
        results['pdf'] = exporter.to_pdf_sim(data, fname, target_name)

    return results
