from jinja2 import Template
import os
from datetime import datetime

class ReportGenerator:
    """
    Executive Report Builder for vulnerability mapping.
    """
    def __init__(self):
        self.template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Executive Vulnerability Report - {{ target_org }}</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f4f4; color: #333; margin: 40px; }
                .container { max-width: 900px; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; }
                h1 { color: #D35400; border-bottom: 2px solid #D35400; padding-bottom: 10px; }
                .risk-high { color: #e74c3c; font-weight: bold; }
                .risk-med { color: #f39c12; }
                .risk-low { color: #27ae60; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background: #121213; color: white; }
                .summary { background: #1A1A1B; color: #E0E0E0; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
                .footer { margin-top: 50px; font-size: 0.8em; color: #777; text-align: center; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Executive Vulnerability Report</h1>
                <div class="summary">
                    <p><strong>Organization:</strong> {{ target_org }}</p>
                    <p><strong>Audit Date:</strong> {{ date }}</p>
                    <p><strong>Overall Risk Score:</strong> {{ overall_risk }} / 1.0</p>
                </div>

                <h2>Departmental Exposure Matrix</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Department</th>
                            <th>Risk Score</th>
                            <th>Vulnerabilities</th>
                            <th>Entities Exposed</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in matrix_data %}
                        <tr>
                            <td>{{ row.department }}</td>
                            <td class="{{ 'risk-high' if row.avg_risk > 0.6 else 'risk-med' if row.avg_risk > 0.3 else 'risk-low' }}">
                                {{ "%.2f"|format(row.avg_risk) }}
                            </td>
                            <td>{{ row.vuln_count }}</td>
                            <td>{{ row.entities_count }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>

                <h2>Security Recommendations</h2>
                <ul>
                    {% for rec in recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>

                <div class="footer">
                    <p>CONFIDENTIAL | Social Engineering Vulnerability Mapper v2.1.0</p>
                    <p>Developed by HSINI MOHAMED</p>
                </div>
            </div>
        </body>
        </html>
        """

    def generate(self, data, output_path):
        template = Template(self.template_str)
        
        # Determine recommendations based on risk
        recs = [
            "Implement mandatory Social Engineering Awareness training for high-risk departments.",
            "Sanitize public-facing professional bios to remove internal tech stack mentions.",
            "Enforce strict privacy settings on employee professional network profiles.",
            "Review public repository commit messages for sensitive internal metadata."
        ]
        
        html_content = template.render(
            target_org=data.get('target_org', 'Global Audit'),
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            overall_risk=data.get('overall_risk', 0.0),
            matrix_data=data.get('matrix_data', []),
            recommendations=recs
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path

if __name__ == "__main__":
    gen = ReportGenerator()
    test_data = {
        "target_org": "ACME Corp",
        "overall_risk": 0.65,
        "matrix_data": [
            {"department": "HR", "avg_risk": 0.8, "vuln_count": 12, "entities_count": 45},
            {"department": "IT", "avg_risk": 0.2, "vuln_count": 2, "entities_count": 10}
        ]
    }
    gen.generate(test_data, "test_report.html")
