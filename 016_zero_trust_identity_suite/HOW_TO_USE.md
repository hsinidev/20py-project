# How to Use: Zero-Trust Identity Verification Suite

## 1. Prerequisites
- Python 3.10+
- A working webcam.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Configuration (First Run)
- On the first run, the system will generate a unique MFA secret.
- Use an app like **Google Authenticator** or **Authy** to scan the QR code (or enter the manual key) provided in the logs/setup view.
- Set your master password for the AES Vault.

## 3. The Trinity Authentication Process
1. **Biometric Scan**: Position your face in front of the camera. The **Cyber-Pulse** ring will glow cyan as it detects and matches your identity.
2. **MFA Token**: Enter the 6-digit code from your authenticator app into the central input field.
3. **Trinity Auth**: Click **INITIATE TRINITY AUTH**. 

## 4. Understanding Results
- **Access Granted (Green)**: All three gates (Face, Token, Key) matched perfectly.
- **Access Denied (Red)**: Any failure in the three gates will block access. Check the status label for specific reasons (e.g., `FACE_MISMATCH` or `MFA_TIMEOUT`).

## 5. Auditing
- Review `data/audit.db` or use the built-in log viewer to see the history of access attempts, including biometric confidence scores.

---
**Developed by HSINI MOHAMED.**
