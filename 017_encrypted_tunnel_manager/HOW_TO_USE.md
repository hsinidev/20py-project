# How to Use: Encrypted Communication Tunnel Manager

## 1. Prerequisites
- Python 3.10+
- **Administrative Privileges** (Required for the Kill-Switch features).
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Setting Up a Tunnel
1. Launch the application: `python main.py`.
2. Select a **Connection Profile** from the dropdown menu.
3. Enter your **Gateway IP** and credentials (if prompted).
4. Click **INITIATE TUNNEL**. The status bar should transition to "ESTABLISHED".

## 3. Activating the Kill-Switch
To prevent data leaks if the connection drops:
- Click **ACTIVATE KILL-SWITCH**.
- The "Security Pulse" will turn orange, indicating the system is now protected.
- In this state, only traffic through the tunnel is allowed.

## 4. Monitoring Traffic
- View the **Tunnel Telemetry** graph at the top of the dashboard.
- Green lines represent inbound data; Orange represents outbound.
- Throughput is updated every 500ms via GPU rendering.

## 5. Stealth Mode
- Use the node selector to choose "Stealth" variants.
- These profiles use obfuscated protocols designed to look like normal HTTPS traffic to bypass corporate or national firewalls.

---
**Developed by HSINI MOHAMED.**
