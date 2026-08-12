# Endpoint Security Policy Auditor (Enterprise Edition)

![Cover](asset/cover.png)

## 🛡️ Overview
The **Endpoint Security Policy Auditor** is a production-grade security tool developed by **HSINI MOHAMED**. It cross-references local machine state against **CIS (Center for Internet Security) Benchmarks** to ensure your workstations and servers are hardened against common attack vectors.

## 🚀 Key Features
- **Asynchronous Audit Engine**: Non-blocking scanning of registry keys, services, and ports.
- **Clinical-Blue UI**: High-fidelity dashboard built with Flet (Python Flutter) featuring glassmorphism.
- **One-Click Remediation**: Instant generation of PowerShell/CLI scripts for non-compliant policies.
- **Health Gauges**: Animated visual metrics representing overall system compliance.
- **Multi-Profile Support**: Switch between 'Workstation' and 'Server' audit configurations.
- **Executive Reporting**: (Planned) PDF and JSON export for audit trails.

## 🛠️ Tech Stack
- **Framework**: Flet (Flutter for Python)
- **Monitoring**: Psutil, WMI
- **Logic**: Asyncio
- **Persistence**: SQLite

## 📥 Installation
```bash
pip install -r requirements.txt
python main.py
```

## 📜 License
Developed for professional security auditing.
**Credit**: Developed by HSINI MOHAMED.
