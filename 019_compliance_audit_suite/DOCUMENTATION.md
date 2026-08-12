# Technical Documentation: Automated Compliance Audit Suite

## 1. Modular Control Architecture
The suite uses a **Modular Control-Validation Architecture (MCVA)**. Compliance frameworks are decoupled from the core engine, defined in YAML files located in `data/frameworks/`. This allows for rapid scaling to new standards (e.g., NIST, GDPR) without code changes.

## 2. Automated Validation Engine
The `SystemAuditor` executes technical checks defined in the framework YAML.
- **Registry Checks**: Verifies OS hardening (e.g., UAC settings, screen lock timeouts).
- **Service Monitoring**: Ensures security services (Antivirus, Firewall) are operational.
- **Log Parsing**: (Extensible) Scans system logs for evidence of specific security events.

## 3. UI/UX Design
Built on **CustomTkinter**, the interface implements a "Sage-Executive" theme:
- **Progress Stepper**: A custom-built 10-step guide that tracks the audit lifecycle from Scoping to Reporting.
- **Matplotlib Integration**: A polar projection gauge provides a professional, semi-circular visualization of the current compliance score.

## 4. Reporting & Persistence
- **Audit Persistence**: All sessions, control statuses, and evidence links are stored in `data/audit_history.db` using SQLite.
- **Document Engine**: Uses `ReportLab` for high-fidelity PDF layouts and `Python-Docx` for editable executive summaries.

## 5. Security & Isolation
The suite is designed to run locally, ensuring that sensitive audit data and evidence documents never leave the organization's perimeter.

---
**Developer**: HSINI MOHAMED
**Version**: 2.5.0
