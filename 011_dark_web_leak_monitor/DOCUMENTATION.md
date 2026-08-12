# Technical Documentation: Dark Web Leak Monitor

## 1. System Architecture
The application follows a **Modular Monolith** pattern, separating the UI layer from the core security and networking logic.

### Components:
- **`main.py`**: The Orchestrator. Manages the CustomTkinter event loop and coordinates between the UI tabs and background threads.
- **`core/tor_engine.py`**: Handles SOCKS5 proxying and circuit management via the Stem library.
- **`core/database.py`**: Manages the encrypted persistence layer using SQLite-Cipher.

## 2. Security Implementation
### Encrypted Storage
The local vault (`assets/vault.db`) uses **AES-256 encryption** via SQLCipher. 
- **Encryption Key**: A tactical-grade key is used for PRAGMA key derivation.
- **Zero-Trust**: No data is stored in plain text. Even keyword configuration is encrypted at rest.

### Panic Protocol
When the **Panic Exit** is triggered:
1. All active scanning threads are flagged for immediate termination.
2. The `TorManager` attempts to signal the Tor process for shutdown.
3. The system cache is cleared before the process exits (Exit Code 0).

## 3. Data Flow
1. **Input**: User enters a sensitive string (Email/API Key).
2. **Encryption**: String is committed to the encrypted database.
3. **Async Scan**: A background worker pulls active keywords and maps them against simulated/live Onion repository responses.
4. **Detection**: Upon regex match, a system interrupt triggers a notification and logs the breach metadata.

## 4. Class Reference

### `DarkWebMonitorApp(ctk.CTk)`
- `_switch_tab(tab_id)`: Manages UI state and visibility.
- `scan_loop()`: The primary asynchronous worker.

### `TorManager`
- `start_tor()`: Establishes the tunnel.
- `query_onion(url)`: Performs a proxied HTTP GET request.

### `EncryptedDB`
- `log_breach(...)`: Securely writes breach data.
- `get_keywords()`: Decrypts and retrieves targets for the scanner.

---
*Developed by HSINI MOHAMED*
