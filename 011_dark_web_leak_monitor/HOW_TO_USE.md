# How to Use: Real-time Dark Web Leak Monitor

## Prerequisites
1. **Python 3.12+**
2. **Tor Browser / Tor Service**: Ensure Tor is running on your machine (default SOCKS5 port: 9050).
3. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup & Operation
1. **Launch**: Run `python main.py`.
2. **Configuration**:
   - Go to the **Tor Gateway** tab to verify your SOCKS5 port settings.
   - Click **Test Tor Connection** to ensure the tunnel is active.
3. **Adding Targets**:
   - In the **Active Scans** tab, enter keywords you want to monitor (e.g., your email, company domain, or specific API keys).
4. **Monitoring**:
   - Click **START GLOBAL SCAN**. The terminal at the bottom will provide real-time feedback.
   - If a match is found, a system notification will trigger, and the event will be logged in the **Breach History** tab.

## Safety Features
- **Panic Exit**: Click the red button in the sidebar to immediately kill the application and close Tor connections.
- **Encrypted Vault**: All your keywords and breach history are stored in an AES-256 encrypted database (`assets/vault.db`).

## Developer Note
Developed by **HSINI MOHAMED**. 
*Disclaimer: This tool is for educational and authorized security monitoring purposes only.*
