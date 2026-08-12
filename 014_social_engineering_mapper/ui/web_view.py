from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import plotly.graph_objects as go
import plotly.io as pio
import tempfile
import os

class RiskHeatmap(QWebEngineView):
    """
    QtWebEngine Bridge for interactive Plotly Heatmaps.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHtml("<html><body style='background:#121213; color:#E0E0E0;'>Loading Heatmap...</body></html>")

    def update_heatmap(self, matrix_data):
        """
        matrix_data: {'z': [[...]], 'x': [...], 'y': [...]}
        """
        if not matrix_data['x']:
            return

        fig = go.Figure(data=go.Heatmap(
            z=matrix_data['z'],
            x=matrix_data['x'],
            y=matrix_data['y'],
            colorscale='Oranges',
            showscale=True
        ))

        fig.update_layout(
            paper_bgcolor='#121213',
            plot_bgcolor='#121213',
            font_color='#E0E0E0',
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(title="Departments"),
            yaxis=dict(showticklabels=False)
        )

        # Export to a temporary HTML file
        temp_file = os.path.join(tempfile.gettempdir(), "risk_heatmap.html")
        # include_plotlyjs=True ensures the library is embedded, fixing "Plotly is not defined"
        pio.write_html(fig, file=temp_file, auto_open=False, include_plotlyjs=True)
        
        self.setUrl(QUrl.fromLocalFile(temp_file))
