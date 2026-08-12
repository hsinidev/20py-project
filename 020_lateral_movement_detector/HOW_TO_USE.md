# How to Use: Network Lateral Movement Detector

## 1. Prerequisites
- Python 3.10+
- **Npcap** (for Windows) or **libpcap** (for Linux) must be installed.
- Administrator/Root privileges are required for packet sniffing and firewall orchestration.

## 2. Installation
```bash
pip install -r requirements.txt
```

## 3. Launching the Detector
1. Run with admin privileges:
   ```bash
   python main.py
   ```
2. Click **INITIALIZE SCANNER** to start listening on the default network interface.

## 4. Monitoring the Topology
- Observe the **Live Topology Map**. Devices are represented as indigo nodes.
- Watch the **Threat Feed** for real-time alerts.
- Suspicious devices will transition to a **Crimson Pulse** state.

## 5. Defense Actions
- If a threat is confirmed, the **Defense Orchestrator** will automatically generate a firewall rule to isolate the node.
- Review the logs in the `logs/` directory for an encrypted forensic trail of all connections.

## 6. Incident Playback
- Use the `ui/traffic_replay.py` module (CLI or via future menu integration) to load `.pcap` files and visualize the attack progression on the graph.

---
**Developed by HSINI MOHAMED.**
