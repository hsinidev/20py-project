import networkx as nx
import pandas as pd

class TopologyManager:
    """
    Graph-based Network Topology Analyzer using NetworkX.
    Maps connections and identifies anomalies in lateral flow.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.flow_data = []

    def add_connection(self, src, dst, weight=1):
        if not self.graph.has_edge(src, dst):
            self.graph.add_edge(src, dst, weight=weight)
        else:
            self.graph[src][dst]['weight'] += weight
            
        self.flow_data.append({"src": src, "dst": dst})

    def get_risk_score(self, src, dst):
        """
        Heuristic: High risk if connection crosses zones or is unusual.
        """
        # Simplistic zone logic: internal vs external
        is_internal_src = src.startswith("192.168.") or src.startswith("10.")
        is_internal_dst = dst.startswith("192.168.") or dst.startswith("10.")
        
        if is_internal_src and is_internal_dst:
            # Check centrality or path length if needed
            return 50 # Default internal risk
        return 20 # Low risk for external outbound

    def get_topology_data(self):
        """Returns nodes and edges for visualization."""
        nodes = [{"id": n, "label": n} for n in self.graph.nodes()]
        edges = [{"from": u, "to": v, "weight": d['weight']} for u, v, d in self.graph.edges(data=True)]
        return nodes, edges

    def analyze_spikes(self):
        if not self.flow_data:
            return pd.DataFrame()
        df = pd.DataFrame(self.flow_data)
        return df.groupby(['src', 'dst']).size().reset_index(name='count')
