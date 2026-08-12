from fpdf import FPDF

class AuditReporter:
    @staticmethod
    def generate_report(campaign_name, stats, output_path="assets/report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Phishing Vulnerability Report: {campaign_name}", 0, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Date: {stats.get('date', '2026-05-13')}", 0, 1)
        pdf.cell(0, 10, f"Total Emails Sent: {stats.get('sent', 0)}", 0, 1)
        pdf.cell(0, 10, f"Total Clicks (CTR): {stats.get('clicks', 0)}", 0, 1)
        pdf.cell(0, 10, f"Compromised Accounts: {stats.get('compromised', 0)}", 0, 1)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Organizational Risk Assessment:", 0, 1)
        pdf.set_font("Arial", '', 12)
        
        risk_level = "Low"
        if stats.get('compromised', 0) > 0:
            risk_level = "High" if stats.get('compromised', 0) > 5 else "Medium"
            
        pdf.multi_cell(0, 10, f"Based on the results, the organizational risk level is currently: {risk_level}.\n"
                               "Recommended Action: Scheduled mandatory security awareness training for all involved users.")
        
        pdf.output(output_path)
        return output_path
