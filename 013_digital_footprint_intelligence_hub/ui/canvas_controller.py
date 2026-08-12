import networkx as nx
import random
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, InstructionGroup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class GraphCanvas(Widget):
    """
    Custom Interactive Node Canvas for Entity Relation Mapping.
    Uses NetworkX for Spring Layout calculations.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.G = nx.Graph()
        self.nodes = {} # {id: {'pos': (x,y), 'color': c, 'label': l}}
        self.edges = []
        self.cyber_cyan = get_color_from_hex("#00F2FF")
        self.found_pulse = get_color_from_hex("#FFB300")
        
        # Center of the widget
        self.center_x = Window.width / 2
        self.center_y = Window.height / 2

    def add_poi(self, label):
        """Add Primary Node (Point of Interest)."""
        node_id = f"poi_{label}"
        self.G.add_node(node_id, type='poi', label=label)
        self.update_layout()

    def add_account(self, poi_label, platform, url):
        """Add discovered account node linked to POI."""
        poi_id = f"poi_{poi_label}"
        acc_id = f"{platform}_{url}"
        self.G.add_node(acc_id, type='account', platform=platform, url=url)
        self.G.add_edge(poi_id, acc_id)
        self.update_layout()

    def update_layout(self):
        """Calculate Spring Layout using NetworkX."""
        if len(self.G.nodes) < 1:
            return

        # Use spring layout for organic positioning
        pos = nx.spring_layout(self.G, k=0.3, iterations=50)
        
        # Scale to widget size
        width = self.width if self.width > 100 else 800
        height = self.height if self.height > 100 else 600
        
        padding = 50
        self.nodes = {}
        for node, (x, y) in pos.items():
            # Normalize to widget coordinates
            nx_pos = (x * (width - padding*2) / 2) + (width / 2)
            ny_pos = (y * (height - padding*2) / 2) + (height / 2)
            self.nodes[node] = {
                'pos': (nx_pos, ny_pos),
                'type': self.G.nodes[node].get('type'),
                'label': self.G.nodes[node].get('label', node)
            }
        
        self.draw_graph()

    def draw_graph(self):
        self.canvas.clear()
        with self.canvas:
            # Draw Edges first
            Color(rgba=[0, 0.95, 1, 0.3])
            for u, v in self.G.edges():
                if u in self.nodes and v in self.nodes:
                    p1 = self.nodes[u]['pos']
                    p2 = self.nodes[v]['pos']
                    # Use absolute coordinates (self.x + pos)
                    Line(points=[self.x + p1[0], self.y + p1[1], self.x + p2[0], self.y + p2[1]], width=1.5)

            # Draw Nodes
            for node_id, data in self.nodes.items():
                pos = data['pos']
                # Use absolute coordinates (self.x + pos)
                if data['type'] == 'poi':
                    # POI Nodes (Glow Cyan)
                    Color(rgba=[0, 0.95, 1, 0.8])
                    Ellipse(pos=(self.x + pos[0]-15, self.y + pos[1]-15), size=(30, 30))
                    # Outer Glow
                    Color(rgba=[0, 0.95, 1, 0.2])
                    Ellipse(pos=(self.x + pos[0]-25, self.y + pos[1]-25), size=(50, 50))
                else:
                    # Account Nodes
                    Color(rgba=[1, 0.7, 0, 0.9])
                    Ellipse(pos=(self.x + pos[0]-10, self.y + pos[1]-10), size=(20, 20))

    def on_size(self, *args):
        self.update_layout()

    def on_pos(self, *args):
        self.draw_graph()

class CanvasController:
    """Manages the graph widget and its interactions."""
    def __init__(self, container):
        self.canvas_widget = GraphCanvas()
        container.add_widget(self.canvas_widget)

    def add_entity(self, label, type='poi', parent=None):
        if type == 'poi':
            self.canvas_widget.add_poi(label)
        elif type == 'account' and parent:
            self.canvas_widget.add_account(parent, label['platform'], label['url'])
