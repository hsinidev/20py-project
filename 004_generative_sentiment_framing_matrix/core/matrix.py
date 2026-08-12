import plotly.express as px
import pandas as pd
import tempfile
import webbrowser

class SentimentMatrix:
    def __init__(self):
        self.data = []

    def add_point(self, brand: str, sentiment: float, authority: float, framing: str):
        self.data.append({
            "Brand": brand,
            "Sentiment": sentiment,
            "Authority": authority,
            "Framing": framing,
            "Size": 10
        })

    def render_3d(self):
        if not self.data: return
        df = pd.DataFrame(self.data)
        
        fig = px.scatter_3d(df, 
                            x='Sentiment', 
                            y='Authority', 
                            z='Brand',
                            color='Framing',
                            size='Size',
                            text='Brand',
                            title='Generative Sentiment & Framing Matrix')

        fig.update_layout(
            template="plotly_dark",
            scene=dict(
                xaxis=dict(backgroundcolor="#1a1a1a", gridcolor="#333", range=[-1,1]),
                yaxis=dict(backgroundcolor="#1a1a1a", gridcolor="#333", range=[0,1]),
                zaxis=dict(backgroundcolor="#1a1a1a", gridcolor="#333")
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        tmp = tempfile.mktemp(suffix=".html")
        fig.write_html(tmp)
        webbrowser.open(tmp)
        return tmp
