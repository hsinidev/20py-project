# Technical Documentation: Endpoint Security Policy Auditor

## 1. System Architecture
The system follows an **Asynchronous Observer Pattern**. The `AuditScanner` acts as the subject, notifying the UI (Flet controls) as each policy check completes in parallel.

## 2. Policy Engine (CIS Benchmarks)
Policies are defined in `engine/cis_benchmarks.py`. Each policy includes:
- `check_type`: registry, service, or port.
- `key/value`: Specific OS identifiers.
- `expected`: The compliant state.
- `remediation`: The PowerShell command to fix the issue.

## 3. Native OS Abstraction (Adapters)
The `engine/adapters/windows_wmi.py` provides a clean interface for:
- `winreg`: Accessing the Windows Registry.
- `psutil`: Querying the Windows Service Control Manager (SCM).
- `socket`: Performing low-latency local port scans.

## 4. UI/UX Design
- **Clinical-Blue Theme**: Uses a high-contrast, clean aesthetic suitable for enterprise security contexts.
- **Reactive States**: Controls transition from 'Auditing' to 'Pass/Fail' dynamically using Flet's state management.
- **Remediation Overlay**: Uses a BottomSheet to display raw scripts safely without cluttering the main dashboard.

## 5. Security & Persistence
- **Audit History**: Historical results are stored in SQLite (implemented in `utils/logger.py`).
- **Data Integrity**: Every check is timestamped and linked to the unique Machine GUID.

---
**Developer**: HSINI MOHAMED
**Version**: 1.5.0
