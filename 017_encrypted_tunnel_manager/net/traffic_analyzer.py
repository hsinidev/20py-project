import time
import random
import threading
from collections import deque

class TrafficAnalyzer:
    """
    Real-time Byte-Stream Telemetry for Tunnel Monitoring.
    """
    def __init__(self, max_points=100):
        self.inbound_data = deque([0]*max_points, maxlen=max_points)
        self.outbound_data = deque([0]*max_points, maxlen=max_points)
        self.running = False
        self.total_received = 0
        self.total_sent = 0

    def start_monitoring(self):
        self.running = True
        self.thread = threading.Thread(target=self._simulate_traffic, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        self.running = False

    def _simulate_traffic(self):
        """
        Simulates real-time traffic updates. 
        In production, this would hook into Scapy or a socket wrapper.
        """
        while self.running:
            # Generate random MB/s values for the Matrix UI
            in_val = random.uniform(0.1, 5.0)
            out_val = random.uniform(0.1, 2.0)
            
            self.inbound_data.append(in_val)
            self.outbound_data.append(out_val)
            
            self.total_received += in_val
            self.total_sent += out_val
            
            time.sleep(0.5)

    def get_data(self):
        return list(self.inbound_data), list(self.outbound_data)
