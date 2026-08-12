# Technical Documentation: Network Lateral Movement Detector

## 1. Packet Processing Pipeline (APPA)
The detector utilizes an **Asynchronous Packet-Pipeline Architecture**. Packets are sniffed using Scapy's `sniff` function in a background thread and fed into a thread-safe queue. A separate consumer thread parses the protocols and extracts behavioral metadata.

## 2. Topology & Graph Heuristics
The `TopologyManager` maintains a Directed Graph (`nx.DiGraph`) where nodes represent IPs and edges represent traffic flows.
- **Weighting**: Edges are weighted by traffic volume and frequency.
- **Anomalies**: Connections between disparate VLANs or zones (e.g., Guest -> Management) trigger high-confidence alerts.

## 3. Dynamic UI Rendering
The dashboard is built with **WxPython**. The network map uses a custom `PaintDC` context to render a live-updating topology.
- **Animations**: A `wx.Timer` drives the "Electric Indigo" pulsing effect by oscillating the radius of the perimeter glow around active nodes.
- **Vector Graphics**: (Integration-ready) Supports `CairoSVG` for high-fidelity export and rendering of complex network maps.

## 4. Defense & Orchestration
The `defense_orchestrator` module interacts with the host's kernel firewall.
- **Windows**: Uses `netsh advfirewall` or `PyWFP` to inject blocking rules.
- **Linux**: Interfaces with `iptables` to drop traffic from flagged source IPs.

## 5. Forensic Logging
All events are serialized into an encrypted forensic audit trail. This allows for post-incident review and satisfies enterprise regulatory requirements for network monitoring.

---
**Developer**: HSINI MOHAMED
**Version**: 3.2.0
