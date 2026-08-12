# How to Use: Endpoint Security Policy Auditor

## 1. Prerequisites
- Python 3.9+
- Administrator privileges (required to read specific registry keys and service statuses).
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Launching the App
1. Open your terminal as Administrator.
2. Run: `python main.py`.

## 3. Performing an Audit
1. Select the **Audit Profile** (Workstation or Server).
2. Click **START SECURITY AUDIT**.
3. Watch the health gauge update in real-time as the scanner checks your system policies.

## 4. Remediation
1. For any item marked as **FAILED**, a red "ONE-CLICK REMEDIATE" button will appear.
2. Click the button to view the exact PowerShell or CLI command needed to fix the vulnerability.
3. Copy the command and execute it in an elevated shell.
4. Re-run the audit to verify compliance.

---
**Developed by HSINI MOHAMED.**
