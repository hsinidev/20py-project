import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ComplianceGauge:
    """
    Renders a semi-circular compliance gauge using Matplotlib.
    """
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.figure, self.ax = plt.subplots(figsize=(4, 2), subplot_kw={'projection': 'polar'})
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.setup_plot()

    def setup_plot(self):
        # Configure the gauge background
        self.ax.set_theta_zero_location("W")
        self.ax.set_theta_direction(-1)
        self.ax.set_thetalim(0, np.pi)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['polar'].set_visible(False)
        self.figure.patch.set_facecolor('#1A1C1E') # Matching background
        self.ax.set_facecolor('#1A1C1E')

    def update_gauge(self, score_percentage):
        self.ax.clear()
        self.setup_plot()
        
        # Draw background arc
        self.ax.bar(np.pi/2, np.pi, width=np.pi, color='#2D3135', bottom=0.8)
        
        # Draw compliance arc
        color = '#87A96B' # Sage Green
        if score_percentage < 40: color = '#FF4B2B' # Red
        elif score_percentage < 70: color = '#D4AF37' # Gold
        
        val = (score_percentage / 100.0) * np.pi
        self.ax.bar(val/2, val, width=val, color=color, bottom=0.8)
        
        # Add text
        self.ax.text(0, -0.5, f"{score_percentage}%", color='#E1E2E5', 
                     ha='center', va='center', fontsize=20, fontweight='bold', transform=self.ax.transAxes)
        self.ax.text(0, -0.7, "COMPLIANCE SCORE", color='#87A96B', 
                     ha='center', va='center', fontsize=10, transform=self.ax.transAxes)
        
        self.canvas.draw()
