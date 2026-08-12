# Technical Documentation: Phishing Simulator

## 1. System Architecture
The application utilizes a **Hybrid Client-Server** model:
- **Client (PyQt6)**: Manages campaign configuration, mail delivery threads, and data visualization.
- **Server (Flask)**: A lightweight local observer that hosts landing pages and captures telemetry.

## 2. Tracking Mechanism
- **JWT Tokens**: Every email contains a unique URL signed with PyJWT.
- **Zero-Data Policy**: The server logs "Clicks" and "Entries" but does **not** store sensitive data submitted through mock forms.

## 3. Core Modules
- **`core/mailer.py`**: Handles SMTP delivery using secure threading to prevent UI lag.
- **`core/database.py`**: Implements a Fernet-based encryption layer for local SQLite storage.
- **`core/reporter.py`**: Transforms campaign data into professional-grade PDF reports.

## 4. Security Controls
- **Legal Splash Screen**: Mandatory startup barrier requiring user acknowledgment of authorized use.
- **Encryption**: Master-key rotation for the local audit database.
