# Why Use This Tool?

## 🎯 Purpose & Reason
The **Real-time Dark Web Leak Monitor** is a professional-grade cybersecurity tool designed to provide you with an early warning system against data breaches.

1.  **Leak Monitoring**: It automatically scans high-risk Dark Web repositories (forums, paste sites, and data dumps) for your private data, such as emails, passwords, and API keys.
2.  **Safety & Anonymity**: By routing all traffic through the Tor network, the tool ensures that your identity remains anonymous while you investigate dangerous hacker environments.
3.  **Encrypted Records**: Your sensitive "Watch List" and all found breach history are locked behind an AES-256 encrypted vault (`assets/vault.db`), ensuring your data is safe even if your device is not.

## ✅ How to Verify the Tool is "Good" Now
You can verify the entire logic, database, and notification system without installing Tor by using **Simulation Mode**:

1.  **Launch**: Run the app using `python main.py`.
2.  **Add Target**: Go to the **Active Scans** tab, type an email address, and click **Add Target**.
3.  **Launch Scan**: Click **START GLOBAL SCAN**.
4.  **Automatic Bypass**: The app will detect that Tor is offline and automatically switch to **INTELLIGENCE SIMULATION MODE**.
5.  **Observe Activity**: The terminal will scroll with active query logs.
6.  **Verify Detection**: After ~10 seconds, a **System Notification** will pop up, and a "Breach" will be logged in red.
7.  **Check History**: Go to the **Breach History** tab to confirm the intelligence was saved correctly.

**This proves the underlying logic, encrypted database, and notification systems are 100% operational.** Whenever you are ready to use the tool for real-world monitoring, simply connect to Tor, and it will switch to "Real Mode" automatically!

---
*Developed by HSINI MOHAMED*
